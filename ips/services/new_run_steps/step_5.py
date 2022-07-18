from flask import request, render_template, session, jsonify
from ips.util.ui_logging import log


from ips.services import app_methods
from ips.services.forms import LoadDataForm, LoadEditDataForm


def run_step_5(run_id):
    from remote_pdb import RemotePdb
    error = False
    run_info = app_methods.get_run(run_id)
    form = LoadDataForm(meta={'survey_file': run_info['SURVEY_FILE'],
        'shift_file': run_info['SHIFT_FILE'],
        'non_response_file': run_info['NR_FILE'],
        'unsampled_file': run_info['UNSAMPLED_FILE'],
        'tunnel_file': run_info['TUNNEL_FILE'],
        'sea_file': run_info['SEA_FILE'],
        'air_file': run_info['AIR_FILE']})
    #RemotePdb('0.0.0.0', 4445).set_trace()
    if form.validate_on_submit():

        log.info("run_step_5 Importing data...")
        # Import Survey Data
        survey_data = request.files['survey_file']
        if survey_data.filename:
            resp = app_methods.import_data('survey', session['id'], survey_data, session['period'], session['year'])
            if resp.status_code != 200:
                error_message = app_methods.get_error_message(resp, "Survey")
                return render_template('new_run_5.html', form=form, error=True, error_message=error_message)
        #elif not survey_data.filename and not :


            log.info("run_step_5 Imported survey data...")

        # Import shift data
        shift_data = request.files['shift_file']
        if shift_data.filename:
            resp = app_methods.import_data('shift', session['id'], shift_data, session['period'], session['year'])
            if resp.status_code != 200:
                error_message = app_methods.get_error_message(resp, "Shift")
                return render_template('new_run_5.html', form=form, error=True, error_message=error_message)

            log.info("run_step_5 Imported shift data...")

        # Import non_response data
        non_response_data = request.files['non_response_file']
        if non_response_data.filename:
            resp = app_methods.import_data('nonresponse', session['id'], non_response_data, session['period'],
                                           session['year'])
            if resp.status_code != 200:
                error_message = app_methods.get_error_message(resp, "Non-Response")
                return render_template('new_run_5.html', form=form, error=True, error_message=error_message)

            log.info("run_step_5 Imported non-response data...")

        # Import un-sampled data
        unsampled_data = request.files['unsampled_file']
        if unsampled_data.filename:
            resp = app_methods.import_data('unsampled', session['id'], unsampled_data, session['period'], session['year'])
            if resp.status_code != 200:
                error_message = app_methods.get_error_message(resp, "Unsampled")
                return render_template('new_run_5.html', form=form, error=True, error_message=error_message)

            log.info("run_step_5 Imported un-sampled data...")

        # Import tunnel data
        tunnel_data = request.files['tunnel_file']
        if tunnel_data.filename:
            resp = app_methods.import_data('tunnel', session['id'], tunnel_data, session['period'], session['year'])
            if resp.status_code != 200:
                error_message = app_methods.get_error_message(resp)
                return render_template('new_run_5.html', form=form, error=True, error_message=error_message)

            log.info("run_step_5 Imported tunnel data...")

        # Import sea data
        sea_data = request.files['sea_file']
        if sea_data.filename:
            resp = app_methods.import_data('sea', session['id'], sea_data, session['period'], session['year'])
            if resp.status_code != 200:
                error_message = app_methods.get_error_message(resp)
                return render_template('new_run_5.html', form=form, error=True, error_message=error_message)
            
            log.info("run_step_5 Imported sea data...")
        # Import air data
        air_data = request.files['air_file']
        if air_data.filename:
            resp = app_methods.import_data('air', session['id'], air_data, session['period'], session['year'])
            if resp.status_code != 200:
                error_message = app_methods.get_error_message(resp)
                return render_template('new_run_5.html', form=form, error=error, error_message=error_message)

            log.info("run_step_5 Imported sair data...")

        if run_id:
            log.debug("step_5: Run_id given...")
            s = f"/manage_run/{run_id}"
            res = {'redirect': s}

            return jsonify(res)
        else:
            log.debug("step_5: No run_id given...")
            res = {'redirect': '/new_run_steps/new_run_5'}
            return jsonify(res)

    # TODO this isn't there
    elif request.method == 'GET':
        log.info("run_step_5 [GET] request")
        return render_template('new_run_5.html',
                               form=form,
                               error=error,
                               run_info=run_info,
                               run_id=run_id)
    else:
        error = True
        log.debug('run_step_5: User did not select files for all input fields')
        error_message = "Select .csv file types for all filename fields"

    return render_template('new_run_5.html', form=form, error=error, error_message=error_message, run_info=run_info, run_id=run_id)
