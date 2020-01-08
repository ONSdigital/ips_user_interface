import json

import requests
import ast
from flask import request, Blueprint, jsonify
import sys

from ips.services import API_TARGET
from ips.util.ui_logging import log

bp = Blueprint('builder', __name__, url_prefix='/builder', static_folder='static')


@bp.route('/<run_id>', methods=['GET', 'POST'])
def create(run_id):
    log.debug("builder: create_run")
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    data = {"json": request.form['json'].strip()}
    # Send PVs
    response = requests.post(API_TARGET + r'/builder/' + run_id, headers=headers, data=data)

    # Validate PVs
    log.debug(f"builder: validate_process_variables: {run_id}")
    response = requests.get(API_TARGET + r'/process_variables/test/' + run_id)

    print(response)

    # Get error message from response
    response_message = json.loads(response.text)
    print(response_message)

    return jsonify(response_message)


@bp.route('/validate', methods=['GET', 'POST'])
def validate():
    code = request.form['pv']
    try:
        ast.parse(code)
        return "Everything's tickety boo", 200
    except SyntaxError as e:
        print(e.lineno)
        return str(e.lineno), 406
