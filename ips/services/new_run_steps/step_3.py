from flask import request, render_template, session, redirect, current_app
from ips.util.ui_logging import log
from ips.services import app_methods

import getpass


def run_step_3(run_id):
    try:
        run_id = session["id"]
    except:
        log.warning("run_step_3: No run_id in session")
        run_id = False

    if request.method == "POST":
        log.debug("run_step_3 [POST] request")
        session["template_id"] = request.form["selected"]

        user = getpass.getuser()

        run_id = session["id"]
        run_name = session["run_name"]
        period = session["period"]
        year = session["year"]

        log.debug(
            "run_step_3 [POST] Session values: %s, %s, %s, %s, %s.",
            run_id,
            run_name,
            period,
            year,
            user,
        )

        app_methods.create_process_variables_set(run_id, run_name, user, period, year)

        session["send"] = 0

        return redirect("/new_run_steps/new_run_4/" + run_id)

    records = app_methods.get_process_variable_sets()

    log.debug(f"Process variable sets: {records}")

    pv_set_id = False

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
        "Q4": "Quarter 4",
        None: "-",
    }

    if run_id:
        for rec in records:
            rec["PERIOD"] = periods[rec["PERIOD"]]
            if rec["RUN_ID"] in run_id:
                pv_set_id = rec["RUN_ID"]

    header = ["RUN_ID", "NAME", "USER", "PERIOD", "YEAR"]

    log.debug("run_step_3 [GET]  Retrieved process variable sets, rendering new_run_3.")

    return render_template(
        "new_run_3.html",
        table=records,
        header=header,
        run_id=run_id,
        pv_set_id=pv_set_id,
    )
