#6/1
from flask import flash  #gpt幫忙新增這行
from sqlalchemy.exc import IntegrityError  #gpt幫忙新增這行
from apps.crud.forms import UserForm
from apps.app import db
from apps.crud.models import User

from flask import Blueprint, render_template, redirect, url_for

crud = Blueprint(
    "crud",
    __name__,
    template_folder="templates",
    static_folder="static",
)


@crud.route("/")
def index():
    return render_template("crud/index.html")

@crud.route("/sql")
def sql():
    db.session.query(User).all()
    return "請確認控制台日誌"

from flask import flash  # ← 新增這行
from sqlalchemy.exc import IntegrityError  # ← 新增這行

@crud.route("/users/new", methods=["GET", "POST"])
def create_user():
    form = UserForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=form.password.data,
        )
        db.session.add(user)
        try:
            db.session.commit()
            return redirect(url_for("crud.users"))
        except IntegrityError:
            db.session.rollback()
            flash("這個 Email 已經被使用過了，請換一個。", "danger")  #gpt幫忙增加功能:顯示錯誤訊息
    return render_template("crud/create.html", form=form)


@crud.route("/users")
def users():
    users = User.query.all()
    return render_template("crud/index.html", users=users)

#6/2
@crud.route("/users/<user_id>", methods=["GET", "POST"])
def edit_user(user_id):
    form = UserForm()

    user = User.query.filter_by(id=user_id).first()

    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("crud.users"))
    
    return render_template("crud/edit.html", user=user, form=form)

@crud.route("/users/<user_id>/delete", methods=["POST"])
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("crud.users"))