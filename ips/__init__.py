import logging

from flask import Flask, redirect, url_for, session
from flask_bootstrap import Bootstrap
from ips.util.ui_logging import log

from ips.services import dashboard, export, manage_run, auth, builder, new_run

from ips.services.extensions import login_manager
from ips.util.ui_configuration import UIConfiguration as Config

host = Config().get_hostname()
port = Config().get_port()

app = Flask(__name__)

login_manager.init_app(app)

Bootstrap(app)

app.config.from_object(Config)

app.logger = logging.getLogger('werkzeug')

app.logger.setLevel(logging.INFO)

app.logger.disabled = True

app.register_blueprint(builder.bp)
app.register_blueprint(auth.bp)
app.register_blueprint(dashboard.bp)
app.register_blueprint(new_run.bp)
app.register_blueprint(manage_run.bp)
app.register_blueprint(export.bp)

log.debug("IPS UI Started")

@app.route('/')
def index():
    session.clear()
    return redirect(url_for('dashboard.dashboard_view'))
