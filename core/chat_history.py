import os
import json
from datetime import datetime
from constants import MESSAGE_HISTORY_CAP, CONVERSATIONS_DIR, EXPRESSIONS
from core.prompt_builder import build_system_prompt

class ChatHistory:
    def __init__(self, conv_id: str = None):
        self.conv_id = conv_id or str(uuid.uuid4())
        self.messages = []
        self._load_if_exists()
    def _load_if_exists(cls):
        filepath = os.path.join(CONVERSATIONS_DIR, f"{self.conv_id}.json")
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                self.messages = data.get('messages', [])
            except Exception:
                self.messages = []

    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})
        self._save()

    def get_messages(self):
        return self.messages

    def _save(self):
        os.makedirs(CONVERSATIONS_DIR, exist_ok=True)
        filepath = os.path.join(CONVERSATIONS_DIR, f"{self.conv_id}.json")

        title = "Untitled"
        for msg in self.messages:
            if msg.get('role') == 'user':
                title = msg.get('content', '')[:50]
                break

        data = {
            "id": self.conv_id,
            "title": title,
            "timestamp": datetime.now().isoformat(),
            "messages": self.messages
        }
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)

    def list_conversations(limit: int = 10) -> list[dict]:
        if not os.path.exists(CONVERSATIONS_DIR):
            return []

        conversations = []
        for filename in os.listdir(CONVERSATIONS_DIR):
            if not filename.endswith(".json"):
                continue
            filepath = os.path.join(CONVERSATIONS_DIR, filename)
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                conv_id = filename.replace(".json", "")
                title = data.get("title", "Untitled")
                if title == "Untitled":
                    for msg in data.get("messages", []):
                        if msg.get("role") == "user":
                            title = msg["content"][:50]
                            break
                conversations.append({
                    "id": conv_id,
                    "title": title,
                    "timestamp": data.get("timestamp", ""),
                    "messages_count": len(data.get("messages", [])),
                })
            except Exception:
                continue

        conversations.sort(key=lambda x: x["timestamp"], reverse=True)
        return conversations[:limit]

    def rename_conversations(conv_id: str, title: str) -> bool:
        filepath = os.path.join(CONVERSATIONS_DIR, f"{conv_id}.json")
        if not os.path.exists(filepath):
            return False
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            data["title"] = title
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=4)
            return True
        except Exception:
            return False