
import os

from flask import Flask

PORT = int(os.environ['PORT']) if 'PORT' in os.environ else 8080

app = Flask(__name__)

@app.route("/")
def main():
    return 'hi'

def start_server():
    app.run(host='0.0.0.0', port=PORT)
