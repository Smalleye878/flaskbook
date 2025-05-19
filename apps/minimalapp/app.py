from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello, Flaskbook!"

@app.route("/hello",
      methods=["GET"],
      endpoint="hello-endpoint")
def hello():
    return "Hello, World!"