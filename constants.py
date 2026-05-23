OLLAMA_API_URL = "http://localhost:11434"
TEXT_MODEL = "gemma3:1b"
VISION_MODEL = "moondream"
VOICE_MODEL = "assets/models/en_GB-semaine-medium.onnx"

OLLAMA_CONFIG = {
    "keep_alive": "-1",
    "num_thread": 4,
    "temperature": 0.7,
    "top_k": 40,
    "top_p": 0.9
}

PERSONA = "ollie"
CHAT_MEMORY_ENABLED = True
MESSAGE_HISTORY_CAP = 10
CONVERSATIONS_DIR = "history"

ENABLE_WEB_ACCESS = True
HOST = "0.0.0.0"
PORT = 8080

LCD_ENABLED = False #Set True when the hardware is connected

EXPRESSIONS = {
    "neutral": "neutral.png",
    "happy": "happy.png",
    "thinking": "thinking.png",
    "listening": "listening.png",
    "speaking": "speaking.png",
    "error": "error.png",
}