from core.response_parser import parse_llm_response
from flask import Flask, request, jsonify
from flask_cors import CORS
from core.llm_client import OllamaClient
from settings.schema import Settings
from settings.store import get_settings, update_settings

app = Flask(__name__)
CORS(app)

# Initialize Ollama client
ollama_client = OllamaClient()

@app.route('/hello/<name>')
def hello_name(name):
    return 'Hello %s!' % name

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Receive a user message, send it to Ollama AI, and return the bot response.
    Expected JSON: {"message": "user input text"}
    """
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        # Check model availability
        if not ollama_client.check_model_availability():
            return jsonify({'error': 'llama3.2:3b model not found. Please pull it first with: ollama pull llama3.2:3b'}), 500
        
        # Generate response
        raw = ollama_client.generate_response(user_message)
        parsed = parse_llm_response(raw)
        
        return jsonify(parsed), 200
        
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'}), 500

@app.route("/api/health")
def health():
    if not hasattr(ollama_client, "health_check"):
        return jsonify({"status": "error", "message": "health_check not implemented"}), 500
    return jsonify(ollama_client.health_check()), 200


@app.get("/api/settings")
def fetch_settings():
    return jsonify(get_settings().dict()), 200

@app.post("/api/settings")
def save_settings():
    data = request.json
    settings = Settings(**data)
    update_settings(settings)
    return jsonify(settings.dict()), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)