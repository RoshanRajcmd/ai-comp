from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import uuid

from utils.llm_client import OllamaClient
from chat_history import get_chat_history, ChatHistory
from settings import Settings, get_settings, update_settings

app = Flask(__name__)
CORS(app)

# --------------------------------------------------
# Initialize Core Services
# --------------------------------------------------

settings = get_settings()
chat_history = get_chat_history()
ollama_client = OllamaClient(model=settings.text_model, chat_history=chat_history)

# Global variable to track current conversation
current_conversation_id = None
current_conversation_messages = []


# --------------------------------------------------
# Chat Endpoint
# --------------------------------------------------

@app.post("/api/chat")
def chat():
    global current_conversation_id, current_conversation_messages
    
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Invalid JSON"}), 400

        user_prompt = data.get("prompt", "").strip()
        conv_id = data.get("conversation_id")  # Get conversation ID from request

        if not user_prompt:
            return jsonify({"error": "Message cannot be empty"}), 400

        # If no conversation ID provided, create a new one
        if not conv_id:
            conv_id = str(uuid.uuid4())
            current_conversation_id = conv_id
            current_conversation_messages = []
        else:
            current_conversation_id = conv_id
            # Load existing conversation if switching
            if conv_id:
                existing = ChatHistory.load_conversation(conv_id)
                if existing:
                    current_conversation_messages = existing.get('messages', [])
                else:
                    current_conversation_messages = []

        # Check model availability
        if not ollama_client.check_model_availability():
            return jsonify({
                "error": f"Model '{ollama_client.model}' not found. Run: ollama pull {ollama_client.model}"
            }), 500

        # Add user message to current conversation
        current_conversation_messages.append({
            "role": "user",
            "content": user_prompt
        })

        # Generate response
        response = ollama_client.chat(user_prompt)

        # Add bot response to current conversation
        if response and 'response' in response:
            current_conversation_messages.append({
                "role": "assistant",
                "content": response['response']
            })
            
            # Save conversation
            ChatHistory.save_conversation(conv_id, current_conversation_messages)

        return jsonify({
            **response,
            "conversation_id": conv_id
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Fetch List of downloaded models in the container
@app.get("/api/list")
def fetch_available_models():
    response = ollama_client.list_models()
    return jsonify(response), 200

# --------------------------------------------------
# Conversation Management
# --------------------------------------------------

@app.get("/api/conversations")
def get_conversations():
    """
    Fetch list of all conversations (last 10)
    """
    try:
        conversations = ChatHistory.get_all_conversations(limit=10)
        return jsonify({"conversations": conversations}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.get("/api/conversations/<conv_id>")
def get_conversation(conv_id: str):
    """
    Load a specific conversation by ID
    """
    try:
        conversation = ChatHistory.load_conversation(conv_id)
        if not conversation:
            return jsonify({"error": "Conversation not found"}), 404
        return jsonify(conversation), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.post("/api/conversations")
def create_conversation():
    """
    Create a new conversation
    """
    try:
        conv_id = str(uuid.uuid4())
        data = request.json or {}
        title = data.get("title", "New Conversation")
        
        # Initialize with empty messages
        messages = []
        ChatHistory.save_conversation(conv_id, messages, title)
        
        return jsonify({
            "id": conv_id,
            "title": title,
            "timestamp": datetime.now().isoformat()
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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
