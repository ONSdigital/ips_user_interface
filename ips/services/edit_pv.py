from flask import request, render_template, Blueprint, jsonify, session
from flask_login import login_required

from ips.services import app_methods
from ips.services.forms import ImportPVForm

from ips.util.ui_logging import log

bp = Blueprint('edit pv', __name__, url_prefix='', static_folder='static')


@bp.route('/edit_pv', methods=['GET', 'POST'])
@bp.route('/edit_pv/<run_id>', methods=['GET', 'POST'])
@bp.route('/edit_pv/<run_id>/<pv_id>', methods=['GET', 'POST'])
@login_required
def edit_pv(run_id, pv_id):
    log.debug(f"edit_pv called - run_id: {run_id}")

    template_id = session['id']
    records = app_methods.get_process_variables(template_id)

    pv = [row['PV_DEF'] for row in records if row['PV_NAME'] == pv_id][0]

    return render_template('edit_pv.html', run_id=run_id, pv_name=pv_id, pv=pv)


@bp.route('/import_pv/<run_id>/<pv_id>', methods=['GET', 'POST'])
@login_required
def import_pv(run_id, pv_id=None):
    log.debug(f"import_pv called - run_id: {run_id}")
    form = ImportPVForm()

    if request.method == "POST":
        log.info("Importing new PV")

        # Import PV
        pv = request.form['pv'];
        pv_json = {'RUN_ID': run_id,
                   'PV_NAME': pv_id,
                   'PV_DEF': pv}

        response = app_methods.edit_single_process_variable(run_id, pv_id, pv_json)

        resp = jsonify(response.ok)
        return resp

    return render_template('import_pv.html', run_id=run_id, form=form, pv_name=pv_id)



