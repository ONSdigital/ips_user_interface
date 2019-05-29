import requests
from flask import request, Blueprint

from ips.services import API_TARGET

bp = Blueprint('builder', __name__, url_prefix='/builder', static_folder='static')


@bp.route('/<run_id>', methods=['GET', 'POST'])
def create(run_id):
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    data = {"json": request.form['json'].strip()}
    response = requests.post(API_TARGET + r'/builder/' + run_id, headers=headers, data=data)
    return ('', 204)
