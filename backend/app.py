from flask import Flask
# requirements.txt: flask-cors
# app.py:
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # Enables CORS for all routes

@app.route('/hello/<name>')
def hello_name(name):
   return 'Hello %s!' % name

if __name__ == '__main__':
   app.run()