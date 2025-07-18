from apps.app import db
from apps.auth.forms import SignUpForm
from apps.crud.models import User
from flask import Blueprint, render_template, flash, url_for, redirect, request
from flask_login import login_user

auth = Blueprint(
    "auth",
    __name__,
    template_folder="templates",
    static_folder="static"
)


@auth.route("/")
def index():
    return render_template("auth/index.html")


#註冊功能端點
@auth.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )

        if user.is_duplicate_email():
            flash("這個郵件位址已經註冊過")
            return redirect(url_for("auth.signup"))
    
        db.session.add(user)
        db.session.commit()
        login_user(user)

        next_ = request.args.get("next")
        if next_ is None or not next_.startswith("/"):
            next_ = url_for("crud.users")
        return redirect(next_)

   
    return render_template("auth/signup.html", form=form)