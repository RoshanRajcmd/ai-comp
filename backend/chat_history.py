import os
import json
from datetime import datetime
from pathlib import Path
from constants import MEMORY_PATH, MAX_MESSAGE_HISTORY, CONVERSATIONS_DIR
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

    @staticmethod
    def get_all_conversations(limit: int = 10):
        """
        Get list of all conversations, sorted by most recent.
        Returns last 'limit' conversations.
        """
        if not os.path.exists(CONVERSATIONS_DIR):
            return []
        
        conversations = []
        for filename in os.listdir(CONVERSATIONS_DIR):
            if filename.endswith('.json'):
                filepath = os.path.join(CONVERSATIONS_DIR, filename)
                try:
                    with open(filepath, 'r') as f:
                        data = json.load(f)
                        # Extract metadata
                        conv_id = filename.replace('.json', '')
                        timestamp = data.get('timestamp', '')
                        messages = data.get('messages', [])
                        
                        # Get title from first user message or generate from timestamp
                        title = "Untitled"
                        for msg in messages:
                            if msg.get('role') == 'user':
                                title = msg.get('content', '')[:50]
                                break
                        
                        conversations.append({
                            'id': conv_id,
                            'title': title,
                            'timestamp': timestamp,
                            'message_count': len(messages)
                        })
                except Exception as e:
                    print(f"Error reading conversation {filename}: {e}")
        
        # Sort by timestamp, most recent first
        conversations.sort(key=lambda x: x['timestamp'], reverse=True)
        return conversations[:limit]
    
    @staticmethod
    def load_conversation(conv_id: str):
        """
        Load a specific conversation by ID.
        """
        filepath = os.path.join(CONVERSATIONS_DIR, f"{conv_id}.json")
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading conversation {conv_id}: {e}")
                return None
        return None
    
    @staticmethod
    def save_conversation(conv_id: str, messages: list, title: str = None):
        """
        Save a conversation with given ID.
        """
        os.makedirs(CONVERSATIONS_DIR, exist_ok=True)
        
        filepath = os.path.join(CONVERSATIONS_DIR, f"{conv_id}.json")
        
        # If title not provided, extract from first user message
        if not title:
            for msg in messages:
                if msg.get('role') == 'user':
                    title = msg.get('content', '')[:50]
                    break
        
        data = {
            'id': conv_id,
            'title': title or 'Untitled',
            'timestamp': datetime.now().isoformat(),
            'messages': messages
        }
        
        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving conversation {conv_id}: {e}")
            return False

# Global singleton
_chat_history = None

def get_chat_history() -> ChatHistory:
    global _chat_history
    if _chat_history is None:
        _chat_history = ChatHistory.load()
    return _chat_history
