# --- APP CONFIGURATION ---
IMAGE_DIR = "./images/"
OLLAMA_API_URL = "http://ollama:11434"
CONFIG_PATH = "config.json"
MEMORY_PATH = "memory.json"
CONVERSATIONS_DIR = "./conversations"
INIT_EXPRESSION = "neutral"
MAX_MESSAGE_HISTORY = 10

DEFAULT_CONFIG = {
    "persona": "neuro",
    "text_model": "gemma3:1b",
    "vision_model": "moondream",
    "voice_model": "piper/en_GB-semaine-medium.onnx",
    "chat_memory": True,
    "camera_rotation": 0,
    "extra_preset_prompt": "",
    "web_access": True,
    "ollama_config": {
        'keep_alive': '-1',
        'num_thread': 4,
        'temperature': 0.7,
        'top_k': 40,
        'top_p': 0.9
    }
}

DEFAULT_RESPONSE = {
    "role": "assistant",
    "response": "",
    "expression": "neutral"
}
