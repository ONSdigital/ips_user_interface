import requests
import ast
from flask import request, Blueprint
import sys

from ips.services import API_TARGET
from ips.util.ui_logging import log

bp = Blueprint('builder', __name__, url_prefix='/builder', static_folder='static')


@bp.route('/<run_id>', methods=['GET', 'POST'])
def create(run_id):
    log.debug("builder: create_run")
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    data = {"json": request.form['json'].strip()}
    response = requests.post(API_TARGET + r'/builder/' + run_id, headers=headers, data=data)
    return '', 204


@bp.route('/validate', methods=['GET', 'POST'])
def validate():
    code = request.form['pv']
    try:
        ast.parse(code)
        return "Everything's tickety boo", 200
    except SyntaxError as e:
        print(e.lineno)
        return str(e.lineno), 406
