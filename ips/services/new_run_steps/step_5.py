from flask import request, render_template, session, jsonify
from ips.util.ui_logging import log
from flask_wtf.file import FileRequired

from ips.services import app_methods
from ips.services.forms import LoadDataForm

def run_step_5(run_id):
    # Build validator dictionary based on values in run_info
    run_info = app_methods.get_run(run_id)
    meta={
        'survey_file': run_info['SURVEY_FILE'],
        'shift_file': run_info['SHIFT_FILE'],
        'non_response_file': run_info['NR_FILE'],
        'unsampled_file': run_info['UNSAMPLED_FILE'],
        'tunnel_file': run_info['TUNNEL_FILE'],
        'sea_file': run_info['SEA_FILE'],
        'air_file': run_info['AIR_FILE']
    }
    form = LoadDataForm(meta=meta)

    error = False
    if request.method == 'GET':
        run_info = app_methods.get_run(run_id)
        log.info("run_step_5 [GET] request")
        return render_template(
            'new_run_5.html',
            form=form,
            error=error,
            run_info=run_info,
            run_id=run_id
        )
    
    error_messages = []
    if form.validate_on_submit():
        log.info("run_step_5 Importing data...")
        # Import Survey Data
        survey_data = request.files['survey_file']
        if survey_data.filename:
            resp = app_methods.import_data('survey', session['id'], survey_data, session['period'], session['year'])
            if resp.status_code != 200:
                error_messages.append(app_methods.get_error_message(resp, "Survey"))
                log.warn("run_step_5 error importing survey data")
            else:
                log.info("run_step_5 Imported survey data...")

        # Import shift data
        shift_data = request.files['shift_file']
        if shift_data.filename:
            resp = app_methods.import_data('shift', session['id'], shift_data, session['period'], session['year'])
            if resp.status_code != 200:
                error_messages.append(app_methods.get_error_message(resp, "Shift"))
                log.warn("run_step_5 error importing shift data")
            else:
                log.info("run_step_5 Imported shift data...")

        # Import non_response data
        non_response_data = request.files['non_response_file']
        if non_response_data.filename:
            resp = app_methods.import_data('nonresponse', session['id'], non_response_data, session['period'],
                                           session['year'])
            if resp.status_code != 200:
                error_messages.append(app_methods.get_error_message(resp, "Non-Response"))
                log.warn("run_step_5 error importing non-response data")
            else:
                log.info("run_step_5 Imported non-response data...")

        # Import un-sampled data
        unsampled_data = request.files['unsampled_file']
        if unsampled_data.filename:
            resp = app_methods.import_data('unsampled', session['id'], unsampled_data, session['period'], session['year'])
            if resp.status_code != 200:
                error_messages.append(app_methods.get_error_message(resp, "Unsampled"))
                log.warn("run_step_5 error importing unsampled data")
            else:
                log.info("run_step_5 Imported unsampled data...")


        # Import tunnel data
        tunnel_data = request.files['tunnel_file']
        if tunnel_data.filename:
            resp = app_methods.import_data('tunnel', session['id'], tunnel_data, session['period'], session['year'])
            if resp.status_code != 200:
                error_messages.append(app_methods.get_error_message(resp, "Tunnel"))
                log.warn("run_step_5 error importing tunnel data")
            else:
                log.info("run_step_5 Imported tunnel data...")

        # Import sea data
        sea_data = request.files['sea_file']
        if sea_data.filename:
            resp = app_methods.import_data('sea', session['id'], sea_data, session['period'], session['year'])
            if resp.status_code != 200:
                error_messages.append(app_methods.get_error_message(resp, "Sea"))
                log.warn("run_step_5 error importing sea data")
            else:
                log.info("run_step_5 Imported sea data...")


        # Import air data
        air_data = request.files['air_file']
        if air_data.filename:
            resp = app_methods.import_data('air', session['id'], air_data, session['period'], session['year'])
            if resp.status_code != 200:
                error_messages.append(app_methods.get_error_message(resp, "Air"))
                log.warn("run_step_5 error importing air data")
            else:
                log.info("run_step_5 Imported air data...")

        if error_messages:
            run_info = app_methods.get_run(run_id)
            return render_template('new_run_5.html', form=form, error=True, error_messages=error_messages, run_info=run_info, run_id=run_id)

        if run_id:
            log.debug("step_5: Run_id given...")
            s = f"/manage_run/{run_id}"
            res = {'redirect': s}

            return jsonify(res)
        else:
            log.debug("step_5: No run_id given...")
            res = {'redirect': '/new_run_steps/new_run_5'}
            return jsonify(res)

    error = True
    log.debug('run_step_5: User did not select files for all input fields')
    error_message = "Select .csv file types for all filename fields"

    return render_template('new_run_5.html', form=form, error=error, error_message=error_message, run_info=run_info, run_id=run_id)
