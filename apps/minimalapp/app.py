#匯入flask,建立flask實體
import logging
import os
from flask_debugtoolbar import DebugToolbarExtension
from flask_mail import Mail, Message
from email_validator import validate_email, EmailNotValidError
from flask import(
    Flask,
    current_app,
    g,
    redirect,
    render_template,
    request,
    url_for,
    flash,
    make_response,
    session,
)

    

app = Flask(__name__)
app.config["SECRET_KEY"]="@AZSMss3p5QPbcY2hBsJ"
#不確定67頁上面是否要打進去
app.logger.setLevel(logging.DEBUG)
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
toolbar = DebugToolbarExtension(app)
#5/31增加Mail類別組態
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
app.config["MAIL_PORT"] = os.environ.get("MAIL_PORT")
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS")
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")

mail = Mail(app)

#5/29確認請求內文
with app.test_request_context("/users?updated=true"):
    print(request.args.get("updated"))

#5/29獲取應用程式內文並加入堆疊
ctx = app.app_context()
ctx.push()

print(current_app.name)

g.connection = "connection"
print(g.connection)


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

#5/30
@app.route("/contact")
def contact():
    response = make_response(render_template("contact.html"))

    response.set_cookie("flaskbook key", "flaskbook value")

    session["username"] = "fomosa"

    return response

@app.route("/contact/complete", methods=["GET", "POST"])
def contact_complete():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        description = request.form["description"]
        is_valid = True

        if not username:
            flash("必須填寫使用者名稱")
            is_valid = False

        if not email:
            flash("必須填寫郵件位址")
            is_valid = False
        
        try:
            validate_email(email)
        except EmailNotValidError:
            flash("請輸入正確格式")
            is_valid = False
        
        if not description:
            flash("必須填寫諮詢內容")
            is_valid = False

        if not is_valid:
            return redirect(url_for("contact"))
        

        send_email(
            email,
            "感謝您來信諮詢。",
            "contact_mail",
            username=username,
            description=description,
        )

        
        flash("諮詢內容已傳送。感謝您來信諮詢。")
        
        return redirect(url_for("contact_complete"))
    
    return render_template("contact_complete.html")

def send_email(to, subject, template, **kwargs):
    msg = Message(subject, recipients=[to])
    msg.body = render_template(template + ".txt", **kwargs)
    msg.html = render_template(template + ".html", **kwargs)
    mail.send(msg)

