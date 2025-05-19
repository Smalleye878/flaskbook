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

@app.route("/hi", methods=["GET", "POST"])
def hi():
    return "Hi,World!"

@app.route("/beautiful/<fomosa>",
    methods=["GET", "POST"],
    endpoint="beautiful-endpoint")
def beautiful(fomosa):
    return f"beautiful, {fomosa}!"