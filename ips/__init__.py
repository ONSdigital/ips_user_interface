import logging

from flask import Flask, redirect, url_for, session, render_template
from flask_bootstrap import Bootstrap
from ips.util.ui_logging import log

from ips.services import dashboard, export, manage_run, auth, builder, new_run, edit_pv

from ips.services.extensions import login_manager
from ips.util.ui_configuration import UIConfiguration as Config

from werkzeug.middleware.proxy_fix import ProxyFix

host = Config().get_hostname()
port = Config().get_port()

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_for=1)

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
app.register_blueprint(edit_pv.bp)

log.debug("IPS UI Started")


@app.errorhandler(Exception)
def internal_server_error(e):
    return render_template("servererror.html"), 500


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


@app.route('/')
def index():
    session.clear()
    return redirect(url_for('dashboard.dashboard_view'))
