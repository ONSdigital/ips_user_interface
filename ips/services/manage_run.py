from datetime import datetime

import requests
from flask import request, render_template, Blueprint, session, redirect, url_for, abort, json
from flask_login import login_required
from ips_common.ips_logging import log

from ips.services import app_methods, API_TARGET
from .forms import ManageRunForm, DataSelectionForm

bp = Blueprint('manage_run', __name__, url_prefix='/manage_run', static_folder='static')

status_values = {
    '0': 'Ready',
    '1': 'Not Started',
    '2': 'Running',
    '3': 'Completed',
    '4': 'Cancelled',
    '5': 'Invalid Run',
    '6': 'Failed'
}

run_types = {
    '0': 'Test',
    '1': 'Live',
    '2': 'Deleted',
    '3': 'SQL',
    '4': 'SQL',
    '5': 'SQL',
    '6': 'SQL'
}

run_statuses = {
    '0': 'Ready',
    '1': 'Not Started',
    '2': 'Running',
    '3': 'Completed',
    '4': 'Cancelled',
    '5': 'Invalid Run',
    '6': 'Failed'
}

periods = {
    "01": "January",
    "02": "February",
    "03": "March",
    "04": "April",
    "05": "May",
    "06": "June",
    "07": "July",
    "08": "August",
    "09": "September",
    "10": "October",
    "11": "Novemeber",
    "12": "December",
    "Q1": "Quarter 1",
    "Q2": "Quarter 2",
    "Q3": "Quarter 3",
    "Q4": "Quarter 4"
}


@bp.route('/start/<run_id>', methods=['POST'])
@login_required
def start_run(run_id):
    form = ManageRunForm()

    run = app_methods.get_run(run_id)
    if not run:
        return json.dumps({'status': 'Error: Run ID not Found'})

    form.validate()

    res = app_methods.start_run(run_id)

    # run_status = app_methods.get_run_steps(run['RUN_ID'])
    #
    # for step in run_status:
    #     step['STEP_STATUS'] = status_values[str(int(step['STEP_STATUS']))]
    #     step['STEP_NUMBER'] = str(int(step['STEP_NUMBER']))

    log.info(f"Start run: {run_id}")
    return json.dumps({'status': 'OK'})


@bp.route('/<run_id>', methods=['GET', 'POST'])
@login_required
def manage_run(run_id):
    form = ManageRunForm()

    run = app_methods.get_run(run_id)
    if not run:
        abort(404)

    session['id'] = run['RUN_ID']
    session['run_name'] = run['RUN_NAME']
    session['run_description'] = run['RUN_DESC']
    session['period'] = run['PERIOD']
    session['year'] = run['YEAR']
    current_run = run

    current_run['RUN_STATUS'] = run_statuses[str(int(current_run['RUN_STATUS']))]
    current_run['RUN_TYPE_ID'] = run_types[str(int(current_run['RUN_TYPE_ID']))]
    current_run['PERIOD'] = periods[run['PERIOD']]
    current_run['LAST_MODIFIED'] = \
        datetime.utcfromtimestamp(current_run['LAST_MODIFIED'] / 1000).strftime('%Y-%m-%d %H:%M:%S')

    # If this is a post then validate if needed
    if request.method == 'POST' and form.validate():
        # If the run button is selected run the calculation steps

        if 'run_button' in request.form:

            res = app_methods.start_run(run_id)

            run_status = app_methods.get_run_steps(run['RUN_ID'])

            for step in run_status:
                step['STEP_STATUS'] = status_values[str(int(step['STEP_STATUS']))]
                step['STEP_NUMBER'] = str(int(step['STEP_NUMBER']))

            return json.dumps({'status': 'OK'})

        elif 'display_button' in request.form:
            return redirect('/manage_run/weights/' + current_run['RUN_ID'], code=302)
        elif 'edit_button' in request.form:
            return redirect('/new_run_steps/new_run_1/' + current_run['RUN_ID'], code=302)
        elif 'export_button' in request.form:
            return redirect('/export_data/' + current_run['RUN_ID'], code=302)
        elif 'manage_run_button' in request.form:
            return redirect('/manage_run/' + current_run['RUN_ID'], code=302)

    log.info("Rendering existing run")

    run_status = app_methods.get_run_steps(run['RUN_ID'])

    for step in run_status:
        step['STEP_STATUS'] = status_values[str(int(step['STEP_STATUS']))]
        step['STEP_NUMBER'] = str(int(step['STEP_NUMBER']))

    return render_template('manage_run.html',
                           form=form,
                           current_run=current_run,
                           run_status=run_status)


@bp.route('/weights/<run_id>', methods=['GET', 'POST'])
@login_required
def weights(run_id=None):
    form = DataSelectionForm()

    run = app_methods.get_run(run_id)
    if run:
        session['id'] = run['RUN_ID']
        session['run_name'] = run['RUN_NAME']
        session['run_description'] = run['RUN_DESC']
        current_run = run

        if request.method == 'POST':
            if form.validate():
                # print(request.values)
                table_name, table_title, data_source = request.values['data_selection'].split('|')
                session['dw_table'] = table_name
                session['dw_title'] = table_title
                session['dw_source'] = data_source
                return redirect(
                    url_for('manage_run.weights_2',
                            table=table_name,
                            id=run['RUN_ID'],
                            source=data_source,
                            table_title=table_title)
                )
        return render_template('weights.html',
                               form=form,
                               current_run=current_run)
    else:
        abort(404)


@bp.route('/weights_2/<id>', methods=['GET', 'POST'])
@bp.route('/weights_2/<id>/<table>/<table_title>/<source>', methods=['GET', 'POST'])
@login_required
def weights_2(id, table=None, table_title=None, source=None):
    if id:
        if table:
            dataframe = app_methods.get_display_data_json(table, id, source)
            file_name = table + ".csv";
            return render_template('weights_2.html',
                                   table_title=table_title,
                                   table_name=table,
                                   table=dataframe,
                                   file_name=file_name,
                                   run_id=id)
        else:
            return redirect(url_for('export.export_data', run_id=id), code=302)
    else:
        abort(404)


@bp.route('/status/<run_id>', methods=['GET'])
@login_required
def status(run_id=None):
    if run_id:
        response = requests.get(API_TARGET + r'/ips-service/status/' + run_id)
        return response.content
    else:
        abort(404)
