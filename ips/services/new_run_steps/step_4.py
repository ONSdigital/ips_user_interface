import getpass
import requests
import json

from flask import request, render_template, session, redirect
from ips.util.ui_logging import log

from ips.services import app_methods, API_TARGET

from ips.util.ui_configuration import UIConfiguration


def run_step_4(run_id, template_id):
    if request.method == 'POST':
        log.debug("run_step_4 [POST] request")

        # Commented out as we update the pv's in the edit/import pv, not here anymore

        # # Method splits a the array into groups of 3
        # def split_list(l, n):
        #     # For item i in a range that is a length of l,
        #     for i in range(0, len(l), n):
        #         # Create an index range for l of n items:
        #         yield l[i:i + n]
        #
        # # String coming from JavaScript
        # data = request.form['pv_data']
        #
        # data = data[:-1]
        #
        # # Split the string by delimiter ^
        # data_list = data.split("^")
        #
        # # Split the list into groups of 3, change 3 to whatever number you need to group by
        # data_array = list(split_list(data_list, 3))
        #
        # # Array will hold the dictionaries
        # data_dictionary_array = []
        #
        # # Iterate over list of lists and create a dictionary for each
        # # Append each dictionary to an array
        #
        # # Process variable id tracking variable
        # pid = 0
        #
        # for array in data_array:
        #     pid += 1
        #     data = {'PROCESS_VARIABLE_ID': pid,
        #             'PV_NAME': array[0],
        #             'PV_DESC': array[1],
        #             'PV_DEF': array[2],
        #             }
        #     data_dictionary_array.append(data)

        user = getpass.getuser()

        log.debug("run_step_4 [POST] Getting session values...")
        # Get required values from the session
        run_id = session['id']
        run_name = session['run_name']
        period = session['period']
        year = session['year']
        if run_id not in app_methods.get_all_run_ids():
            log.info("New run_id given, creating new process variable set...")

            # Creates a new set of process variables, then fill the empty set with the edited javascript data
            app_methods.create_process_variables_set(run_id, run_name, user, period, year)

        session['template_id'] = run_id
        log.debug("run_step_4 [POST] Session values: %s, %s, %s, %s, %s.", run_id, run_name, period, year, user)
        print("redirect4")
        return redirect('/new_run_steps/new_run_5/' + run_id)

    if template_id is None:
        template_id = session['template_id']

    run_id = session['id']

    header = ['PV_NAME', 'PV_REASON', 'PV_CONTENT']

    records = app_methods.get_process_variables(template_id)

    print('render new run 4 now')
    return render_template('new_run_4.html', run_id=run_id, table=records,
                           header=header, api_target=API_TARGET,)
