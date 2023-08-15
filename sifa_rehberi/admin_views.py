from flask_admin import Admin, AdminIndexView,expose
from flask_admin.contrib import sqla
from flask_babel import gettext
from flask_login import current_user
from flask_security import utils
from markupsafe import Markup,escape
from werkzeug.utils import redirect
from wtforms import PasswordField,ValidationError,StringField
from wtforms.validators import  Optional,DataRequired
from model import Bitki, Role, User, Recete, Hastalik
from sifa_rehberi import app, db


class CommonModel(sqla.ModelView):
    def is_accessible(self):
        return current_user.has_role("admin")


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.has_role("admin")


admin = Admin(
    app,
    name="Şifa Rehberi Admin",
    template_mode="bootstrap4",
    base_template="admin/base_admin.html",
    index_view=MyAdminIndexView()
)

#admin.add_view(CommonModel(Role,db.session))
