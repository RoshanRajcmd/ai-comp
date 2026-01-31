import requests
from core.prompt_builder import build_system_prompt
from settings.store import get_settings

class OllamaClient:
    def __init__(self, base_url="http://ollama:11434", model="llama3.2:3b"):
        self.base_url = base_url
        self.model = model

        # Build system prompt ONCE
        self.system_prompt = build_system_prompt()

        # Optional: conversation memory
        self.history = []

    def refresh_system_prompt(self):
        """
        Call this when settings (mode, chaos, etc.) change
        """
        self.system_prompt = build_system_prompt()
        self.history.clear()  # optional but recommended

    def check_model_availability(self):
        response = requests.get(f"{self.base_url}/api/tags", timeout=5)
        response.raise_for_status()
        models = [m["name"] for m in response.json().get("models", [])]
        return self.model in models

    def generate_response(self, user_input: str):
        prompt = self._build_prompt(user_input)

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

        response = requests.post(
            f"{self.base_url}/api/generate",
            json=payload,
            timeout=120
        )
        response.raise_for_status()

        output = response.json().get("response", "").strip()

        # Store history (optional, but very Neuro-like)
        self.history.append(("user", user_input))
        self.history.append(("assistant", output))

        return output
    
    def health_check(self):
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            response.raise_for_status()
            return {
                "status": "ok",
                "ollama": "connected",
                "model": self.model
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def _build_prompt(self, user_input: str) -> str:
        """
        Combine system prompt + short conversation context
        """
        history_text = ""
        for role, msg in self.history[-6:]:
            history_text += f"{role.upper()}: {msg}\n"

        return f"""
{self.system_prompt}

{history_text}
USER: {user_input}
ASSISTANT:
""".strip()
