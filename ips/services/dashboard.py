from flask_login import login_required
from flask import request, render_template, Blueprint, redirect
from datetime import datetime

from ips.util.ui_logging import log

from .forms import SearchActivityForm
from ips.services import app_methods

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard', static_folder='static')


@bp.route('/', methods=['GET', 'POST'])
@login_required
def dashboard_view():
    form = SearchActivityForm()

    # Log that dashboard view has been accessed
    log.debug('Dashboard being accessed...')

    # Get the records and separate the headers and values
    try:
        records = app_methods.get_runs()
    except Exception as error:
        log.error(error, exc_info=True)
        return redirect("/")  # return the actual error and display it

    header = [
        'Run_Name',
        'Run_Description',
        'Period',
        'Year',
        'Modified',
        'User',
        'Status',
        'Options'
    ]

    if len(records) == 0:
        return render_template('dashboard.html',
                               header=header,
                               records=records,
                               form=form)

    records.sort(key=lambda x: x['LAST_MODIFIED'])

    # Setup key value pairs for displaying run information
    run_types = {
        '0': 'Test',
        '1': 'Live',
        '2': 'Deleted',
        '3': 'SQL',
        '4': 'SQL',
        '5': 'SQL',
        '6': 'SQL'
    }

    run_statuses = {
        '0': 'Ready',
        '1': 'Not Started',
        '2': 'Running',
        '3': 'Completed',
        '4': 'Cancelled',
        '5': 'Invalid Run',
        '6': 'Failed'
    }

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
        "Q4": "Quarter 4"
    }
    print("here")

    # Reformat values to be displayed on the UI
    for record in records:
        record['RUN_STATUS'] = run_statuses[str(int(record['RUN_STATUS']))]
        record['RUN_TYPE_ID'] = run_types[str(int(record['RUN_TYPE_ID']))]
        record['PERIOD'] = periods[record['PERIOD']]
        record['LAST_MODIFIED'] = datetime.utcfromtimestamp(record['LAST_MODIFIED'] / 1000).strftime('%d/%m/%Y %H:%M:%S')

    # If this is a post then validate if needed
    if request.method == 'POST' and form.validate():
        log.debug("dashboard [POST] request")
        print("1")
        print(request.form)
        # If the search button is selected filter the results on the run status and the searched word.
        if 'search_button' in request.form:
            print("here")
            print(request)
            search_activity = request.form['search_activity']
            filter_value = request.form['run_type_filter']
            log.debug(f"dashboard search request, search term {search_activity}, filter: {filter_value}")

            def fil(x):

                return (
                        search_activity.lower() in x['RUN_NAME'].lower() or
                        search_activity.lower() in x['RUN_DESC'].lower() or
                        search_activity.lower() in x['PERIOD'].lower() or
                        search_activity.lower() in x['USER_ID'].lower() or
                        search_activity.lower() in str(x['YEAR'])
                )

            records = filter(fil, records)

            # If the filer is -1 then no filter to apply otherwise filter using the run_status value
            if request.form['run_type_filter'] != '-1':
                records = filter(lambda x: x['RUN_STATUS'].lower() == run_statuses[filter_value].lower(), records)

    log.debug('dashboard: Rendering dashboard now...')

    return render_template('dashboard.html',
                           header=header,
                           records=records,
                           form=form)


def fil(search_activity, x):
    return (
            search_activity.lower() in x['RUN_ID'].lower() or
            search_activity.lower() in x['RUN_NAME'].lower() or
            search_activity.lower() in x['RUN_DESC'].lower() or
            search_activity.lower() in x['PERIOD'].lower() or
            search_activity.lower() in str(x['YEAR'])
    )
