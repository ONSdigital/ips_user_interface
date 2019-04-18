import io
import os
import zipfile
from flask import request, render_template, Blueprint, session, redirect, send_file, abort
from flask_login import login_required
from ips.persistence.app_methods import create_export_data_download
from ips.persistence.app_methods import export_clob
from ips.persistence.app_methods import get_export_data_table
from ips.persistence.app_methods import get_run
from ips.persistence.forms import ExportSelectionForm

bp = Blueprint('export', __name__, url_prefix='', static_folder='static')


@bp.route('/reference_export/<run_id>', methods=['GET', 'POST'])
@bp.route('/reference_export/<run_id>/<new_export>/<msg>', methods=['GET', 'POST'])
@login_required
def reference_export(run_id, new_export="0", msg="", data=""):
    run_statuses = {'0': 'Ready', '1': 'In Progress', '2': 'Completed', '3': 'Failed'}

    # Retrieve run information
    run = get_run(run_id)

    if run:
        session['id'] = run['RUN_ID']
        session['run_name'] = run['RUN_NAME']
        session['run_description'] = run['RUN_DESC']
        current_run = run

        current_run['RUN_STATUS'] = run_statuses[str(int(current_run['RUN_STATUS']))]

        # Retrieve table data
        try:
            data = get_export_data_table(run_id)
        except Exception as err:
            print(err)

        # Generate New Export button
        if request.method == 'POST':
            return redirect('/export_data/' + run_id)

        return render_template('reference_export.html',
                               current_run=current_run,
                               data=data,
                               new_export=str(new_export),
                               msg=str(msg))
    else:
        abort(404)


@bp.route('/export_data/<run_id>/<file_name>/<source_table>', methods=['DELETE', 'GET', 'POST'])
@bp.route('/export_data/<run_id>', methods=['GET', 'POST', 'DELETE'])
@login_required
def export_data(run_id):
    if run_id:
        form = ExportSelectionForm()
        run = get_run(run_id)

        session['id'] = run['RUN_ID']
        session['run_name'] = run['RUN_NAME']
        session['run_description'] = run['RUN_DESC']

        current_run = run

        if request.method == 'POST' and form.validate():
            # Get values from front end
            sql_table = request.values['data_selection']

            if not create_export_data_download(run_id, sql_table):
                return render_template('export_data.html', form=form,
                                       current_run=current_run,
                                       data="0")
            return redirect('/reference_export/' + run_id)

        elif request.method == 'POST':
            if 'cancel_button' in request.form:
                return redirect('/reference_export/' + current_run['RUN_ID'], code=302)

        return render_template('export_data.html', form=form,
                               current_run=current_run, data="1")

    else:
        abort(404)


@bp.route('/download_data/<run_id>/<file_name>/<source_table>')
@login_required
def download_data(run_id, file_name, source_table):
    if run_id:
        # Assign variables
        memory_file = io.BytesIO()

        # Export source table as clob
        export_clob(run_id, file_name, source_table)

        # Zip file (# source = file to be zipped. file_name = zip name)
        zipfile.ZipFile(memory_file, mode='w').write(file_name + ".csv")
        memory_file.seek(0)
        os.remove(file_name + ".csv")

        return send_file(memory_file, attachment_filename='{}.zip'.format(file_name))

    else:
        abort(404)
