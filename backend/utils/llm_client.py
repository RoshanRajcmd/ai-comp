import requests
import json
import datetime
from typing import Dict, Any

from constants import OLLAMA_API_URL, DEFAULT_CONFIG
from utils.prompt_builder import build_init_system_prompt
from chat_history import get_chat_history


class OllamaClient:
    def __init__(
            self,
            base_url: str = OLLAMA_API_URL,
            model: str = DEFAULT_CONFIG["text_model"],
            chat_history = get_chat_history()
    ):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.chat_history = chat_history

    # --------------------------------------------------
    # System Prompt
    # --------------------------------------------------

    def refresh_system_prompt(self):
        """
        Rebuild system prompt (call when personality/settings change)
        """
        new_prompt = build_init_system_prompt()
        self.chat_history.permanent_memory[0] = {
            "role": "assistant",
            "content": new_prompt
        }
        self.chat_history.session_memory.clear()

    def list_models(self):
        print("Model in OllamaClient: ", self.model)
        response = requests.get(
            f"{self.base_url}/api/tags",
            timeout=10
        )
        response.raise_for_status()

        data = response.json()

        # Extract model names safely
        models = [model["name"] for model in data.get("models", [])]

        return models

    def check_model_availability(self) -> bool:
        print("Checking Model availability")
        models = self.list_models()
        return self.model in models

    # --------------------------------------------------
    # Core Chat
    # --------------------------------------------------

    def chat(self, user_input: str) -> Dict[str, Any]:
        print("Generating")

        # Add user message
        self.chat_history.add_message("user", user_input)

        messages = (
                self.chat_history.permanent_memory
                + self.chat_history.session_memory
        )

        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False
        }
        print("Payload: {}".format(payload))
        
        response = requests.post(
            f"{self.base_url}/api/chat",
            json=payload,
        )
        response.raise_for_status()

        output = response.json()["message"]["content"].strip()

        print("Model response: {}".format(output))

        # Save assistant response
        self.chat_history.add_message("assistant", output)
        self.chat_history.commit_session()
        self.chat_history.save()

        return self._parse_llm_response(output)

    # --------------------------------------------------
    # Response Parsing
    # --------------------------------------------------

    def _parse_llm_response(self, raw: str) -> Dict[str, Any]:
        """
        If model returns JSON, parse it.
        Otherwise fallback to plain text.
        """
        try:
            data = json.loads(raw)
            return {
                "response": data.get("response", ""),
                "expression": data.get("expression", "neutral")
            }
        except Exception:
            return {
                "response": raw,
                "expression": "neutral"
            }

    # --------------------------------------------------
    # Tool Execution
    # --------------------------------------------------

    def execute_action(self, action_data: Dict[str, Any]) -> str:
        action = action_data.get("action", "").lower().strip()
        value = action_data.get("value") or action_data.get("query")

        if action == "get_time":
            now = datetime.datetime.now().strftime("%I:%M %p")
            return f"The current time is {now}."

        if action == "search_web":
            # You can plug DuckDuckGo here
            return f"(Search result placeholder for '{value}')"

        if action == "capture_image":
            return "Image captured."

        return "INVALID_ACTION"
