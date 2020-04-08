from flask import request, render_template, session, redirect

from ips.services import app_methods, API_TARGET


def run_step_4(run_id, template_id):
    if request.method == 'POST':
        return redirect('/new_run_steps/new_run_5/' + run_id)

    run_id = session['id']

    header = ['PV_NAME', 'PV_REASON', 'PV_CONTENT']

    records = app_methods.get_process_variables(run_id)

    return render_template('new_run_4.html', run_id=run_id, table=records,
                           header=header, api_target=API_TARGET,)
