import urllib

from flask import request
from flask_babel import gettext, lazy_gettext
from flask_security.forms import NextFormMixin
from flask_security.utils import verify_and_update_password
from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, StringField

from model import User


class LoginForm(FlaskForm, NextFormMixin):
    password = PasswordField("password")
    remember = BooleanField(lazy_gettext("Remember me"))
    submit = SubmitField("login")
    requires_confirmation = False

    def init(self, args, **kwargs):
        super().init(args, kwargs)
        self.user = None
        if not self.next.data:
            self.next.data = request.args.get("next", "")
        if not self.next.data and request.referrer and request.referrer.contains("next="):
            self.next.data = urllib.parse.unquote(request.referrer).split("next=")[1]
        self.remember.default = True
        self.form_errors = []

    def validate(self, kwargs):
        raise NotImplementedError()

    def check_user(self):
        if self.user is None or not self.user.password:
            return False, gettext("User was not found")
        if not self.user.is_active:
            return False, gettext("Disabled account")
        return True, ""

    def _check_password(self):
        if not self.password.data or self.password.data.strip() == "":
            return False, gettext("You did not enter a password")
        if not verify_and_update_password(self.password.data, self.user):
            return False, gettext("Password is wrong")
        return True, ""

    def _get_checker_method_names(self):
        return [method_name for method_name in dir(self) if method_name.startswith("check_")]

    def checker(self):
        is_success, message = self.check_user()
        if not is_success:
            self.form_errors.append(message)
            return False

        checker_method_names = self._get_checker_method_names()

        for method_name in checker_method_names:
            checking_method = getattr(self, method_name)
            is_success, message = checking_method()
            if not is_success:
                self.form_errors.append(message)
                return False

        return True


class LoginByEmailForm(LoginForm):
    """
    Email login form. Derives from LoginForm. Used to log-in via email address.
    """

    email = StringField("email")

    def validate(self, **kwargs):
        if not self.email.data or self.email.data.strip() == "":
            self.form_errors.append(gettext("You did not enter your email"))
            return False

        self.user = User.query.filter_by(email=self.email.data).first()
        return self.checker()
