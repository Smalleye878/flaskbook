#匯入flask,建立flask實體
from flask import Flask, render_template, url_for

app = Flask(__name__)

#5/19配對網址和執行的函數
@app.route("/")
def index():
    return "Hello, Flaskbook!"

#5/19使用端點#5/22修改在/hello後加/<name>，這個不會和其他衝突，是屬於這個route的參數名
@app.route("/hello/<name>",
      methods=["GET"],
      endpoint="hello-endpoint")
def hello(name):
    return f"Hello, {name}!"

#5/19使用路由建置
@app.route("/hi", methods=["GET", "POST"])
def hi():
    return "Hi,World!"

#5/19指定變數
@app.route("/beautiful/<fomosa>",
    methods=["GET", "POST"],
    endpoint="beautiful-endpoint")
def beautiful(fomosa):
    return f"beautiful, {fomosa}!"

#5/22建立show_name端點
@app.route("/name/<Name>")
def show_name(Name):
    return render_template("index.html", name=Name)
#這裡我有搞混name跟Name，其實一個代表的是變數name一個是我輸入的Name，再對應到index裡

#5/22輸出url_for
with app.test_request_context():
    print(url_for("index"))
    print(url_for("hello-endpoint", name="world"))
    print(url_for("show_name", Name="fomosa", page="1"))#執行出來會是/name/fomosa?page=1，而?後面屬於額外資料
