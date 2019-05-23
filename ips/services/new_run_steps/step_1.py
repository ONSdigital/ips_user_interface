from flask import request, render_template, session, redirect
from ips_common.ips_logging import log

from ips.services import app_methods
from ips.services.forms import CreateRunForm


def run_step_1(run_id):
    log.info("Accessing new_run_1...")
    form = CreateRunForm()
    # if request is a post
    if request.method == 'POST' and form.validate():
        if request.form['submit'] == 'create_run':

            session['run_name'] = request.form['run_name']
            session['run_description'] = request.form['run_description']

            if run_id:
                log.info("Run_id given, editing existing run.")
                run = app_methods.get_run(run_id)

                run['RUN_NAME'] = request.form['run_name']
                run['RUN_DESC'] = request.form['run_description']
                # Update run name and description
                app_methods.edit_run(run_id=run_id, run_name=run['RUN_NAME'], run_description=run['RUN_DESC'],
                                     period=run['PERIOD'], year=run['YEAR'], run_type=run['RUN_TYPE_ID'],
                                     run_status='0')

                log.debug("Updated existing run details.")
                log.info("Redirecting to new_run_2...")

                return redirect('/new_run_steps/new_run_2/' + run_id, code=302)
            else:
                log.info("Run_id not given. Creating new run.")
                log.info("Redirecting to new_run_2...")
                # Generate new run id and store name and description to be used in run creation
                return redirect('/new_run_steps/new_run_2', code=302)
    else:
        # If request is a GET
        if run_id:
            run = app_methods.get_run(run_id)
            form.run_name.default = run['RUN_NAME']
            form.run_description.default = run['RUN_DESC']

    if form.run_name.errors or form.run_description.errors:
        log.warning("Missing valid run_id or description.")

    return render_template('new_run_1.html', form=form, run_id=run_id)
