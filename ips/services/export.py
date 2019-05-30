import io
import os
import zipfile

from flask import request, render_template, Blueprint, session, redirect, send_file, abort, Response
from flask_login import login_required

from ips.services.app_methods import create_export_data_download
from ips.services.app_methods import export_clob
from ips.services.app_methods import get_run
from ips.services.forms import ExportSelectionForm

bp = Blueprint('export', __name__, url_prefix='', static_folder='static')


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
            if 'cancel_button' in request.form:
                return redirect('/manage_run/' + current_run['RUN_ID'], code=302)
            sql_table = request.values['data_selection']
            csv = create_export_data_download(run_id, sql_table)
            if not csv:
                return render_template('export_data.html', form=form,
                                       current_run=current_run,
                                       data="0")
            else:
                return Response(
                    csv,
                    mimetype="text/csv",
                    headers={"Content-disposition": "attachment; filename=" + sql_table})

        elif request.method == 'POST':
            if 'cancel_button' in request.form:
                return redirect('/manage_run/' + current_run['RUN_ID'], code=302)

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