import getpass
import uuid

from flask import request, render_template, session, redirect
from ips.util.ui_logging import log

from ips.services import app_methods
from ips.services.forms import MonthSelectionForm, QuarterSelectionForm


def run_step_2_m(run_id):
    form = MonthSelectionForm()
    new_run = True

    # if request is a post
    if request.method == 'POST':
        log.debug("run_step_2 [POST] request")
        session['period'] = request.form['s_month']

        if form.validate():
            if request.form['submit'] == 'create_run':
                global period

                period = request.form['s_month']

                session['period'] = period

                if run_id:
                    # Update run start and end dates
                    run = app_methods.get_run(run_id)
                    run['PERIOD'] = period

                    app_methods.edit_run(run_id=run_id, run_name=run['RUN_NAME'], run_description=run['RUN_DESC'],
                                         period=run['PERIOD'], year=run['YEAR'],
                                         run_type=run['RUN_TYPE_ID'], run_status='0')
                    log.debug("run_step_2 [POST] Run edited with start and end date. Redirecting to new_run_3...")

                    return redirect('/new_run_steps/new_run_3/' + run_id, code=302)
                else:
                    unique_id = uuid.uuid4()
                    session['id'] = str(unique_id)
                    log.debug("run_step_2 [POST] Generated new unique_id.")
                    app_methods.create_run(session['id'], session['run_name'], session['run_description'],
                                           getpass.getuser(),
                                           session['period'], session['year'])
                    log.debug("run_step_2 [POST] New run created from session variables. Redirecting to new_run_3...")

                    return redirect('/new_run_steps/new_run_3/' + session['id'], code=302)

    errors = form.errors
    last_entry = {}

    if 's_day' in session:
        last_entry['s_month'] = session['s_month']
    else:
        last_entry['s_month'] = ""

    if run_id:
        new_run = False
        run = app_methods.get_run(run_id)
        last_entry['s_month'] = run['PERIOD']

        form.s_month.default = run['PERIOD']
        form.process()
    return render_template('new_run_2_m.html',
                           form=form,
                           last_entry=last_entry,
                           run_id=run_id, new_run=new_run)


def run_step_2_q(run_id):
    form = QuarterSelectionForm()
    new_run = True

    # if request is a post
    if request.method == 'POST':
        log.debug("run_step_2 [POST] request")
        session['period'] = request.form['s_quarter']

        if form.validate():
            if request.form['submit'] == 'create_run':
                global period

                period = request.form['s_quarter']

                session['period'] = period

                if run_id:
                    # Update run start and end dates
                    run = app_methods.get_run(run_id)
                    run['PERIOD'] = period
                    # run['YEAR'] = end_date

                    app_methods.edit_run(run_id=run_id, run_name=run['RUN_NAME'], run_description=run['RUN_DESC'],
                                         period=run['PERIOD'], year=run['YEAR'],
                                         run_type=run['RUN_TYPE_ID'], run_status='0')
                    log.debug("run_step_2 [POST] Run edited with start and end date. Redirecting to new_run_3...")

                    return redirect('/new_run_steps/new_run_3/' + run_id, code=302)
                else:
                    unique_id = uuid.uuid4()
                    session['id'] = str(unique_id)
                    log.debug("run_step_2 [POST] Generated new unique_id.")
                    app_methods.create_run(session['id'], session['run_name'], session['run_description'],
                                           getpass.getuser(),
                                           session['period'], session['year'])
                    log.debug("run_step_2 [POST] New run created from session variables. Redirecting to new_run_3...")

                    return redirect('/new_run_steps/new_run_3/' + session['id'], code=302)

    errors = form.errors
    last_entry = {}

    if 's_day' in session:
        last_entry['s_quarter'] = session['s_quarter']
    else:
        last_entry['s_quarter'] = ""

    if run_id:
        new_run = False
        run = app_methods.get_run(run_id)
        last_entry['s_quarter'] = run['PERIOD']

        form.s_quarter.default = run['PERIOD']
        form.process()

    print('render step 2 quarter')
    return render_template('new_run_2_q.html',
                           form=form,
                           last_entry=last_entry,
                           run_id=run_id, new_run=new_run)
