import requests
from flask import request, Blueprint
from ips.util.ui_configuration import UIConfiguration

API_TARGET = UIConfiguration().get_api_uri()
bp = Blueprint('builder', __name__, url_prefix='/builder', static_folder='static')

@bp.route('/<run_id>/<pv_id>', methods=['GET', 'POST'])
def new_run_5(run_id, pv_id):
    print(request.form)
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    data = {"json" : request.form['json'],"pv": request.form['pv'], 'pv_name' : request.form['pv_desc'], 'pv_desc' : request.form['pv_desc']}
    print(data)
    response = requests.post(API_TARGET + r'/builder/'+run_id+'/'+pv_id, headers=headers, data=data)