#註冊功能表單
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length

#建立註冊功能表單類別
class SignUpForm(FlaskForm):
    username = StringField(
        "使用者名稱",
        validators=[
            DataRequired("必須填寫使用者名稱。"),
            Length(1, 30,"請勿輸入超過30個字元。"),
        ],   
    )
    email = StringField(
        "郵件位址",
        validators=[
            DataRequired("必須填寫郵件位址"),
            Email("請依照電子郵件位址格式輸入。"),
        ],
    )
    password = PasswordField("密碼",
        validators=[DataRequired("必須填寫密碼。")])
    submit = SubmitField("提交表單") 