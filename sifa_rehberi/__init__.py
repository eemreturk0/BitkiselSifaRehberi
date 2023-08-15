from flask import Flask,session,request
from flask_login import LoginManager
from flask_security import Security, SQLAlchemyUserDatastore
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'

db = SQLAlchemy(app)

login_manager = LoginManager(app)
from model import User, Role


user_datastore=SQLAlchemyUserDatastore(db,User,Role)
from account_forms import LoginByEmailForm

security = Security(app, user_datastore,login_form=LoginByEmailForm)
def get_locale():
    if "locale" in session:
        return session["locale"]
    return request.accept_languages.best_match(("en", "tr"), "tr")
babel=Babel(app,locale_selector=get_locale)
def initialize_db_and_folders():
    db.create_all()
    user_datastore.find_or_create_role(name="admin",description="Administrator")
    if User.query.first() is None:
        user_datastore.create_user(password="password",email="deneme@example.com")
        admin_user=user_datastore.create_user(password="password",email="admin@example.com")
        user_datastore.add_role_to_user(admin_user,"admin")
        user_datastore.commit()
@app.after_request
def after_request(response):
    """
    Adds this header to each response.
    This means the client can send accept ranges with units of bytes when requesting a file.
    """
    response.headers.add("Accept-Ranges", "bytes")
    response.headers.add("Strict-Transport-Security", "max-age=63072000; includeSubDomains; preload")
    response.headers.add("Referrer-Policy", "same-origin")
    return response


from . import api_views # noqa
from . import general_views # noqa
from . import admin_views # noqa

with app.app_context():
    initialize_db_and_folders()
