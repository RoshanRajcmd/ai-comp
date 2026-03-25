import os
import json
from constants import MEMORY_PATH, MAX_MESSAGE_HISTORY
from utils.prompt_builder import build_init_system_prompt

class ChatHistory:
    def __init__(self, system_prompt: str):
        # First message is always system prompt
        self.permanent_memory = [{"role": "assistant", "content": system_prompt}]
        self.session_memory = []

    @classmethod
    def load(cls):
        """
        Load chat history from disk.
        Always returns a ChatHistory object.
        """
        if os.path.exists(MEMORY_PATH):
            try:
                with open(MEMORY_PATH, "r") as f:
                    data = json.load(f)

                if isinstance(data, list) and len(data) > 0:
                    system_prompt = data[0]["content"]
                    instance = cls(system_prompt)
                    instance.permanent_memory = data
                    return instance

            except Exception:
                pass

        # Fallback if file missing or corrupted
        return cls(build_init_system_prompt())

    def save(self):
        """
        Save last 10 conversation messages + system prompt.
        """
        full = self.permanent_memory + self.session_memory

        # Keep system prompt separate
        system = full[0]
        conversation = full[1:]

        # Keep only last 10 messages
        if len(conversation) > MAX_MESSAGE_HISTORY:
            conversation = conversation[-MAX_MESSAGE_HISTORY:]

        with open(MEMORY_PATH, "w") as f:
            json.dump([system] + conversation, f, indent=4)

    def add_message(self, role: str, content: str):
        """
        Add message to current session memory.
        """
        self.session_memory.append({
            "role": role,
            "content": content
        })

    def commit_session(self):
        """
        Move session memory into permanent memory.
        """
        self.permanent_memory.extend(self.session_memory)
        self.session_memory = []

# Global singleton
_chat_history = None

def get_chat_history() -> ChatHistory:
    global _chat_history
    if _chat_history is None:
        _chat_history = ChatHistory.load()
    return _chat_history
