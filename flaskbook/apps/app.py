import logging
import os
from flask_login import LoginManager
from apps.config import config
from pathlib import Path
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from email_validator import validate_email, EmailNotValidError
from flask_debugtoolbar import DebugToolbarExtension
from flask_mail import Mail, Message
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
app.debug = True
app.config["SECRET_KEY"]= "2AZSMss3p5QPbcY2hBsJ"
app.logger.setLevel(logging.DEBUG)
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
toolbar = DebugToolbarExtension(app)
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
app.config["MAIL_PORT"] = os.environ.get("MAIL_PORT")
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS")
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")


mail = Mail(app)

@app.route("/")
def index():
    return "Hello, Flaskbook"

@app.route("/hello")
def hello():
    return "Hello, World!"

@app.route("/hello/<name>",
  methods=["GET", "POST"],
  endpoint="hello-endpoint")
def hello(fomosa):
    return f"Hello, {fomosa}!"

@app.route("/name/<Name>")
def show_name(Name):
    return render_template("index.html", name=Name)

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
            flash("請輸入正確的郵件格式")
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


        flash("諮詢內容已送達。感謝您來信詢問。")
        
        return redirect(url_for("contact_complete"))

       
    return render_template("contact_complete.html")

def send_email(to, subject, template, **kwargs):
    msg = Message(subject, recipients=[to])
    msg.body = render_template(template + ".txt", **kwargs)
    msg.html = render_template(template + ".html", **kwargs)
    mail.send(msg)

with app.test_request_context():
    print(url_for("index"))
    print(url_for("hello-endpoint", name="world"))
    print(url_for("show_name", Name="fomosa", page="1"))


with app.test_request_context("/users?updated=true"):
    print(request.args.get("updated"))

ctx = app.app_context()
ctx.push()

print(current_app.name)

g.connection = "connection"
print(g.connection)


csrf = CSRFProtect()

db = SQLAlchemy()

#login部分
login_manager = LoginManager()
login_manager.login_view = "auth.signup"
login_manager.login_message = ""

def create_app():
    app = Flask(__name__)
    from apps.crud import views as crud_views
    app.config.from_mapping(
        SECRET_KEY="2AZSMss3p5QPbcY2hBsJ",
        SQLALCHEMY_DATABASE_URI="sqlite:////" +
        str(Path(Path(__file__).parent.parent, "local.sqlite")),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_ECHO=True,
        WTF_SECRET_KEY="AumzyszU5sugKN7KZs6f",
    )

    csrf.init_app(app)


def create_app(config_key):
    app = Flask(__name__)
  
    app.config.from_object(config[config_key])


    from apps.auth import views as auth_views

    app.register_blueprint(auth_views.auth, url_prefix="/auth")

    return app
    login_manager.init_app(app)






    







