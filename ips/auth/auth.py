from base64 import b64encode

import requests
from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_user, logout_user

from ips.auth.forms import LoginForm
from ips.auth.models import User
from ips.util.ui_configuration import UIConfiguration
from ips.persistence.extensions import login_manager

bp = Blueprint('auth', __name__, template_folder='templates')

API_TARGET = UIConfiguration().get_api_uri() + "/login/"


@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = request.form['username']
        password = request.form['password']

        pwd = b64encode(password.encode('ascii')).decode('ascii')
        print(API_TARGET)
        validation = requests.get(API_TARGET + username + '/' + pwd)

        if validation.status_code == 404:
            # Invalid username
            return render_template("login.html", form=form)

        if validation.status_code == 401:
            # Invalid password
            return render_template("login.html", form=form)

        if validation.status_code == 200:
            # Successful login
            user = User(username=form.username.data)
            login_user(user)
            return redirect(request.args.get("next") or url_for("dashboard.dashboard_view"))

    return render_template("login.html", form=form)


@bp.route("/logout")
def logout():
    logout_user()

    return redirect(url_for("auth.login"))


# callback to reload the user object
@login_manager.user_loader
def load_user(userid):
    return User(userid)
