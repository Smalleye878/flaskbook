#匯入flask,建立flask實體
from flask import Blueprint, render_template


crud = Blueprint(
    "crud",
    __name__,
    template_folder="templates",
    static_folder="static",
)


@crud.route("/")
def index():
    return render_template("crud/index.html")

#5/31 crud開始實作
def create_app():
    app = Flask(__name__)
    from apps.crud import views as crud_views

    app.register_blueprint(crud_views.crud, url_prefix="/crud")


    return app
