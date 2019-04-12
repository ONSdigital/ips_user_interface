from flask_login import login_required
from flask import request, render_template, Blueprint, current_app, redirect
from datetime import datetime
from .forms import SearchActivityForm
from ips.persistence import app_methods

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard', static_folder='static')


@bp.route('/', methods=['GET', 'POST'])
@login_required
def dashboard_view():
    form = SearchActivityForm()

    # Log that dashboard view has been accessed
    current_app.logger.info('Dashboard being accessed...')

    # Get the records and separate the headers and values
    try:
        records = app_methods.get_runs()
    except Exception as error:
        current_app.logger.error(error, exc_info=True)
        return redirect("/")  # return the actual error and display it

    header = [
        'Run_ID',
        'Run_Name',
        'Run_Description',
        'Period',
        'Year',
        'Modified',
        'User',
        'Status'
    ]

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
        '1': 'In Progress',
        '2': 'Completed',
        '3': 'Failed'
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

    # Reformat values to be displayed on the UI
    for record in records:
        record['RUN_STATUS'] = run_statuses[str(int(record['RUN_STATUS']))]
        record['RUN_TYPE_ID'] = run_types[str(int(record['RUN_TYPE_ID']))]
        record['PERIOD'] = periods[record['PERIOD']]
        record['LAST_MODIFIED'] = datetime.utcfromtimestamp(record['LAST_MODIFIED'] / 1000).strftime(
            '%Y-%m-%d %H:%M:%S')

    # If this is a post then validate if needed
    if request.method == 'POST' and form.validate():

        # If the search button is selected filter the results on the run status and the searched word.
        if 'search_button' in request.form:
            search_activity = request.form['search_activity']
            filter_value = request.form['run_type_filter']
            # If the filer is -1 then no filter to apply otherwise filter using the run_status value
            if request.form['run_type_filter'] != '-1':
                records = [x for x in records
                           if (search_activity.lower() in x['RUN_ID'].lower() or
                               search_activity.lower() in x['RUN_NAME'].lower() or
                               search_activity.lower() in x['RUN_DESC'].lower() or
                               search_activity.lower() in x['PERIOD'].lower() or
                               search_activity.lower() in x['YEAR'].lower()) and
                           run_statuses[filter_value].lower() == x['RUN_STATUS'].lower()]
            else:
                records = [x for x in records
                           if search_activity.lower() in x['RUN_ID'].lower() or
                           search_activity.lower() in x['RUN_NAME'].lower() or
                           search_activity.lower() in x['RUN_DESC'].lower() or
                           search_activity.lower() in x['PERIOD'].lower() or
                           search_activity.lower() in x['YEAR'].lower()]

    current_app.logger.info('Rendering dashboard now...')

    return render_template('dashboard.html',
                           header=header,
                           records=records,
                           form=form)
