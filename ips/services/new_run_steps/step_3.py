from flask import request, render_template, session, redirect, current_app

from ips.services import app_methods


def run_step_3(run_id):
    try:
        run_id = session['id']
    except:
        run_id = False

    if request.method == "POST":
        session['template_id'] = request.form['selected']

        current_app.logger.info("Redirecting to new_run_4 with template_id " + session['template_id'] + "...")

        return redirect('/new_run_steps/new_run_4')

    records = app_methods.get_process_variable_sets()

    pv_set_id = False

    periods = {"01": "January",
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
               "Q4": "Quarter 4",
               None: "-"}

    if run_id:
        for rec in records:
            rec['PERIOD'] = periods[rec['PERIOD']]
            if rec['RUN_ID'] in run_id:
                pv_set_id = rec['RUN_ID']

    header = ['RUN_ID', 'NAME', 'USER', 'PERIOD', 'YEAR']

    current_app.logger.debug("Retrieved process variable sets, rendering new_run_3.")

    return render_template('new_run_3.html', table=records, header=header)