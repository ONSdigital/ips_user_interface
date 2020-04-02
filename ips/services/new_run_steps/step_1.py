from flask import request, render_template, session, redirect
from ips.util.ui_logging import log

from ips.services import app_methods
from ips.services.forms import CreateRunForm


def run_step_1(run_id):
    new_run = True
    form = CreateRunForm()
    # if request is a post
    if request.method == 'POST' and form.validate():
        if request.form['submit'] == 'create_run':
            log.debug("run_step_1 [POST] request")

            global year

            year = request.form['run_year']
            period_type = request.form['run_period_type']
            session['run_name'] = request.form['run_name']
            session['run_description'] = request.form['run_description']
            session['year'] = year
            session['run_period_type'] = period_type

            if run_id:
                log.debug("run_step_1 [POST] Run_id given, editing existing run.")
                run = app_methods.get_run(run_id)

                run['RUN_NAME'] = request.form['run_name']
                run['RUN_DESC'] = request.form['run_description']
                run['YEAR'] = request.form['run_year']

                # Update run name and description
                app_methods.edit_run(run_id=run_id, run_name=run['RUN_NAME'], run_description=run['RUN_DESC'],
                                     period=run['PERIOD'], year=run['YEAR'], run_type=run['RUN_TYPE_ID'],
                                     run_status='0')

                log.debug("run_step_1 [POST] Updated existing run details.")
                log.info("run_step_1 [POST] Redirecting to new_run_2...")

                if period_type == 'Month':
                    return redirect('/new_run_steps/new_run_2_m/' + run_id, code=302)
                else:
                    return redirect('/new_run_steps/new_run_2_q/' + run_id, code=302)
            else:
                log.debug("run_step_1 [POST]  Run_id not given. Creating new run.")
                log.debug("run_step_1 [POST]  Redirecting to new_run_2...")
                # Generate new run id and store name and description to be used in run creation
                if period_type == "Month":
                    return redirect('/new_run_steps/new_run_2_m', code=302)
                else:

                    return redirect('/new_run_steps/new_run_2_q', code=302)
    else:
        # If request is a GET
        log.debug("run_step_1 [GET] request")
        if run_id:
            run = app_methods.get_run(run_id)
            print(run)
            form.run_name.default = run['RUN_NAME']
            form.run_description.default = run['RUN_DESC']
            form.run_year.default = run['YEAR']
            print(run['PERIOD'][0])
            if run['PERIOD'][0] == 'Q':
                form.run_period_type.default = 'Quarter'
            else:
                form.run_period_type.default = 'Month'
            new_run = False

    if form.run_name.errors or form.run_description.errors:
        log.warning("run_step_1 [GET] Missing valid run_id or description.")

    print("renderrrr")
    return render_template('new_run_1.html', form=form, run_id=run_id, new_run=new_run)
