from base64 import b64encode

import requests
from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_user, logout_user

from ips.services import API_TARGET
from .extensions import login_manager
from .forms import LoginForm
from .models import User

bp = Blueprint('auth', __name__, template_folder='templates')


@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = request.form['username']
        password = request.form['password']

        pwd = b64encode(password.encode('ascii')).decode('ascii')
        validation = requests.get(API_TARGET + f"/login/{username}/{pwd}")

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
