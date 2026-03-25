from flask import Flask, request, jsonify
from flask_cors import CORS

from utils.llm_client import OllamaClient
from chat_history import get_chat_history
from settings import Settings, get_settings, update_settings

app = Flask(__name__)
CORS(app)

# --------------------------------------------------
# Initialize Core Services
# --------------------------------------------------

settings = get_settings()
chat_history = get_chat_history()
ollama_client = OllamaClient(model=settings.text_model, chat_history=chat_history)


# --------------------------------------------------
# Chat Endpoint
# --------------------------------------------------

@app.post("/api/chat")
def chat():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Invalid JSON"}), 400

        user_prompt = data.get("prompt", "").strip()

        if not user_prompt:
            return jsonify({"error": "Message cannot be empty"}), 400

        # Check model availability
        if not ollama_client.check_model_availability():
            return jsonify({
                "error": f"Model '{ollama_client.model}' not found. Run: ollama pull {ollama_client.model}"
            }), 500

        # Generate response
        response = ollama_client.chat(user_prompt)

        return jsonify(response), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Fetch List of downloaded models in the container
@app.get("/api/list")
def fetch_available_models():
    response = ollama_client.list_models()
    return jsonify(response), 200

# --------------------------------------------------
# Fetch Chat History
# --------------------------------------------------

@app.get("/api/history")
def fetch_history():
    return jsonify({
        "permanent_memory": chat_history.permanent_memory,
        "session_memory": chat_history.session_memory
    }), 200


# --------------------------------------------------
# Settings
# --------------------------------------------------

@app.get("/api/settings")
def fetch_settings():
    return jsonify(get_settings().model_dump()), 200


@app.post("/api/settings")
def save_settings():
    data = request.json

    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        new_settings = Settings(**data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    changed_fields = update_settings(new_settings)

    # If model or personality changed → refresh system prompt
    if "text_model" in changed_fields:
        ollama_client.model = new_settings.text_model

    if "personality" in changed_fields or "mode" in changed_fields:
        ollama_client.refresh_system_prompt()

    return jsonify(get_settings().model_dump()), 200


# --------------------------------------------------
# App Start
# --------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
