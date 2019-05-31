from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor
from flask_moment import Moment
from flask_login import LoginManager

db = SQLAlchemy()
moment = Moment()
ckeditor = CKEditor()
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    from myblog.models import Admin
    user = Admin.query.get(int(user_id))
    return user
