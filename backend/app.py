from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)

# Ollama API endpoint - using 'ollama' as hostname since it's a docker service
OLLAMA_BASE_URL = "http://ollama:11434"

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
        
        # First, ensure the model is available
        try:
            models_response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
            available_models = [m['name'] for m in models_response.json().get('models', [])]
            
            if 'llama3.2:3b' not in available_models:
                return jsonify({'error': 'llama3.2:3b model not found. Please pull it first with: ollama pull llama3.2:3b'}), 500
        except Exception as e:
            return jsonify({'error': f'Cannot check available models: {str(e)}'}), 500
        
        # Call Ollama AI running on port 11434
        payload = {
            "model": "llama3.2:3b",
            "prompt": user_message,
            "stream": False
        }
        
        response = requests.post(f"{OLLAMA_BASE_URL}/api/generate", json=payload, timeout=120)
        response.raise_for_status()
        
        result = response.json()
        bot_response = result.get('response', 'No response from AI').strip()
        
        return jsonify({
            'success': True,
            'response': bot_response,
            'user_message': user_message
        }), 200
        
    except requests.exceptions.ConnectionError as e:
        return jsonify({'error': f'Cannot connect to Ollama service: {str(e)}'}), 500
    except requests.exceptions.Timeout:
        return jsonify({'error': 'Ollama request timed out. The model may be loading.'}), 500
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Ollama API error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'}), 500

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint to verify Ollama connectivity"""
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        if response.status_code == 200:
            return jsonify({'status': 'ok', 'ollama': 'connected'}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Ollama not responding properly'}), 500
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Cannot reach Ollama: {str(e)}'}), 500
        return jsonify({'error': f'Error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)