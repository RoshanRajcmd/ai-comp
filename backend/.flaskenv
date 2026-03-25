# Specifies the Python file that contains your Flask application instance (app = Flask(__name__))
FLASK_APP=app.py

# Sets the environment to development, enabling debug mode and live reloader.
FLASK_ENV=development

# URL for the Ollama API, referencing the service name used in docker-compose.yml
# This is crucial for your backend to find the Ollama container when running via Docker Compose.
