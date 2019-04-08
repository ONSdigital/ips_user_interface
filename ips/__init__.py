import logging

from flask import Flask, redirect, url_for, session
from flask_bootstrap import Bootstrap

from ips.persistence import dashboard, export, new_run, manage_run, system_info, auth
from ips.persistence.extensions import login_manager
from ips.util.ui_configuration import UIConfiguration as Config

host = Config().get_hostname()
port = Config().get_port()


def create_app():
    app = Flask(__name__)

    login_manager.init_app(app)

    Bootstrap(app)

    app.config.from_object(Config)

    # ma = Marshmallow()
    # ma.init_app(app)

    app.logger = logging.getLogger('werkzeug')

    app.logger.setLevel(logging.INFO)

    app.logger.disabled = True

    app.register_blueprint(auth.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(system_info.bp)
    app.register_blueprint(new_run.bp)
    app.register_blueprint(manage_run.bp)
    app.register_blueprint(export.bp)

    @app.route('/')
    def index():
        session.clear()
        return redirect(url_for('dashboard.dashboard_view'))

    return app
