from flask import request, render_template, Blueprint
from flask_login import login_required
from ips.persistence import app_methods

bp = Blueprint('system_info', __name__, url_prefix='/system_info', static_folder='static')


@bp.route('/')
@login_required
def system_info():
    print(request.method)
    records = app_methods.get_system_info()
    header = records[0]
    records = records[1:]

    return render_template('system_info.html',
                           header=header,
                           records=records)
