import os
import uuid
import getpass
import pwd
from flask import request, render_template, Blueprint, session, redirect, current_app
from flask_login import login_required
from ips.persistence import app_methods
from .forms import CreateRunForm, DateSelectionForm, LoadDataForm


bp = Blueprint('new_run', __name__, url_prefix='/new_run', static_folder='static')


@bp.route('/new_run_1', methods=['GET', 'POST'])
@bp.route('/new_run_1/<run_id>', methods=['GET', 'POST'])
@login_required
def new_run_1(run_id=None):
    current_app.logger.info("Accessing new_run_1...")
    form = CreateRunForm()
    # if request is a post
    if request.method == 'POST' and form.validate():
        if request.form['submit'] == 'create_run':

            session['run_name'] = request.form['run_name']
            session['run_description'] = request.form['run_description']

            if run_id:
                current_app.logger.info("Run_id given, editing existing run.")
                run = app_methods.get_run(run_id)

                run['RUN_NAME'] = request.form['run_name']
                run['RUN_DESC'] = request.form['run_description']
                # Update run name and description
                app_methods.edit_run(run_id=run_id, run_name=run['RUN_NAME'], run_description=run['RUN_DESC'],
                                     period=run['PERIOD'], year=run['YEAR'], run_type=run['RUN_TYPE_ID'],
                                     run_status='0')

                current_app.logger.debug("Updated existing run details.")
                current_app.logger.info("Redirecting to new_run_2...")

                return redirect('/new_run/new_run_2/' + run_id, code=302)
            else:
                current_app.logger.info("Run_id not given. Creating new run.")
                current_app.logger.info("Redirecting to new_run_2...")
                # Generate new run id and store name and description to be used in run creation
                return redirect('/new_run/new_run_2', code=302)
    else:
        # If request is a GET
        if run_id:
            run = app_methods.get_run(run_id)
            form.run_name.default = run['RUN_NAME']
            form.run_description.default = run['RUN_DESC']

    if form.run_name.errors or form.run_description.errors:
        current_app.logger.warning("Missing valid run_id or description.")

    return render_template('new_run_1.html',
                           form=form,
                           run_id=run_id)


@bp.route('/new_run_2', methods=['GET', 'POST'])
@bp.route('/new_run_2/<run_id>', methods=['GET', 'POST'])
@login_required
def new_run_2(run_id=None):
    form = DateSelectionForm()

    # if request is a post
    if request.method == 'POST':
        current_app.logger.debug("Processing post request.")
        session['period'] = request.form['s_month']
        session['year'] = request.form['s_year']

        if form.validate():
            if request.form['submit'] == 'create_run':

                global start_date
                global end_date

                start_date = request.form['s_month']
                end_date = request.form['s_year']

                session['period'] = start_date
                session['year'] = end_date

                if run_id:
                    # Update run start and end dates
                    run = app_methods.get_run(run_id)
                    run['PERIOD'] = start_date
                    run['YEAR'] = end_date
                    app_methods.edit_run(run_id=run_id, run_name=run['RUN_NAME'], run_description=run['RUN_DESC'],
                                         period=run['PERIOD'], year=run['YEAR'],
                                         run_type=run['RUN_TYPE_ID'], run_status='0')
                    current_app.logger.info("Run edited with start and end date. Redirecting to new_run_3...")

                    return redirect('/new_run/new_run_3/' + run_id, code=302)
                else:
                    unique_id = uuid.uuid4()
                    session['id'] = str(unique_id)
                    current_app.logger.debug("Generated new unique_id.")
                    app_methods.create_run(session['id'], session['run_name'], session['run_description'],
                                           getpass.getuser(),
                                           session['period'], session['year'])
                    current_app.logger.info("New run created from session variables. Redirecting to new_run_3...")

                    return redirect('/new_run/new_run_3/' + session['id'], code=302)

    errors = form.errors
    last_entry = {}

    if 's_day' in session:
        last_entry['s_month'] = session['s_month']
        last_entry['s_year'] = session['s_year']
    else:
        last_entry['s_month'] = ""
        last_entry['s_year'] = ""

    if run_id:
        run = app_methods.get_run(run_id)
        last_entry['s_month'] = run['PERIOD']
        last_entry['s_year'] = run['YEAR']

        form.s_month.default = run['PERIOD']
        form.s_year.default = run['YEAR']
        form.process()

    return render_template('new_run_2.html',
                           form=form,
                           last_entry=last_entry,
                           run_id=run_id)


# TODO: Implement edit run functionality when how we're dealing with files is determined.
@bp.route('/new_run_5', methods=['GET', 'POST'])
@bp.route('/new_run_5/<run_id>', methods=['GET', 'POST'])
@login_required
def new_run_5(run_id=None):
    form = LoadDataForm()
    csv_error = False
    serial_error = False
    column_error = False
    date_error = False

    if form.validate_on_submit():

        # Functionality has been written. Stubbed for now as we are unsure yet as to the location and method
        # of storing the csv's in a file system. Until we can access DAP and know where to store, this will remain.
        # The below code shows the method for retrieving the filename and data from the uploaded files.

        # Import survey data
        # survey_data = form.survey_file.data
        # stream = io.StringIO(survey_data.stream.read().decode("UTF8"), newline=None)
        # survey_csv = csv.DictReader(stream)
        # survey_csv.fieldnames = [name.upper() for name in survey_csv.fieldnames]
        # survey_json = list(survey_csv)
        # print(survey_json)
        # app_methods.import_data('SHIFT_DATA', session['id'], survey_json)

        # TODO: Duplicates causing issues with imports (Returning 500)... need to look into dealing with this. @TM

        # External
        current_app.logger.debug("Clearing down table records...")
        # Clear down table records associated with the current run id
        # app_methods.delete_data('SHIFT_DATA', session['id'])
        # app_methods.delete_data('NON_RESPONSE_DATA', session['id'])
        # app_methods.delete_data('UNSAMPLED_OOH_DATA', session['id'])
        # app_methods.delete_data('TRAFFIC_DATA', session['id'])

        current_app.logger.debug("Finished clearing down table records.")

        current_app.logger.info("Importing data...")

        # Import survey data
        survey_data = form.survey_file.data
        survey_error = app_methods.survey_data_import('survey', session['id'], survey_data, start_date, end_date)

        serial_error = survey_error[0]
        date_error = survey_error[1]
        # column_error = survey_error[2]

        # Import shift data
        shift_data = form.shift_file.data
        app_methods.external_survey_data_import('shift', session['id'], shift_data)

        # Import non_response data
        non_response_data = form.non_response_file.data
        app_methods.external_survey_data_import('nonresponse', session['id'], non_response_data)

        # Import unsampled data
        unsampled_data = form.unsampled_file.data
        app_methods.external_survey_data_import('unsampled', session['id'], unsampled_data)

        # Import tunnel data
        tunnel_data = form.tunnel_file.data
        app_methods.external_survey_data_import('tunnel', session['id'], tunnel_data)

        # Import sea data
        sea_data = form.sea_file.data
        app_methods.external_survey_data_import('sea', session['id'], sea_data)

        # Import air data
        air_data = form.air_file.data
        app_methods.external_survey_data_import('air', session['id'], air_data)

        if serial_error is False and date_error is False: #and column_error is False
            if run_id:
                current_app.logger.debug("Run_id given...")
                return redirect('/manage_run/' + run_id)
            else:
                current_app.logger.debug("No run_id given...")
                return redirect('/new_run/new_run_5', code=302)
        else:
            if serial_error:
                current_app.logger.warning('Survey Data - Serial column does not exist or is invalid.')
                print("Serial column does not exist or is invalid")
            elif date_error:
                current_app.logger.warning('Survey Data - Dating error - Start date in '
                                           'input does not match start dates in file.')
                column_error = False
                print("Start dates in survey data should reflect start dates in the uploaded file.")
            # elif column_error:
            #     current_app.logger.warning('Survey Data - Incorrect number of columns.')
            #     serial_error = False
            #     print("Survey Data file should contain 212 columns.")

    elif request.method == 'GET':
        current_app.logger.info("Fulfilling GET request...")
        return render_template('new_run_5.html',
                               form=form,
                               error=csv_error,
                               run_id=run_id)
    else:
        csv_error = True
        current_app.logger.warning('User did not fill all fields with .csv files.')

    return render_template('new_run_5.html', form=form, csv_error=csv_error,
                           serial_error=serial_error, column_error=column_error, date_error=date_error)


@bp.route('/new_run_3', methods=['GET', 'POST'])
@bp.route('/new_run_3/<run_id>', methods=['GET', 'POST'])
@login_required
def new_run_3(run_id = None):
    try:
        run_id = session['id']
    except:
        run_id = False

    if request.method == "POST":
        session['template_id'] = request.form['selected']

        current_app.logger.info("Redirecting to new_run_4 with template_id " + session['template_id'] + "...")

        return redirect('/new_run/new_run_4')

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


@bp.route('/edit')
@login_required
def edit(row=None):
    return render_template('edit.html', row=row)


@bp.route('/new_run_4', methods=['GET', 'POST'])
@bp.route('/new_run_4/<run_id>', methods=['GET', 'POST'])
@login_required
def new_run_4(run_id = None):
    if request.method == 'POST':

        current_app.logger.info("Getting data from Javascript modal...")

        # Method splits a the array into groups of 3
        def split_list(l, n):
            # For item i in a range that is a length of l,
            for i in range(0, len(l), n):
                # Create an index range for l of n items:
                yield l[i:i + n]

        # String coming from JavaScript
        data = request.form['pv_data']

        data = data[:-1]

        # Split the string by delimiter ^
        data_list = data.split("^")

        # Split the list into groups of 3, change 3 to whatever number you need to group by
        data_array = list(split_list(data_list, 3))

        # Array will hold the dictionaries
        data_dictionary_array = []

        # Iterate over list of lists and create a dictionary for each
        # Append each dictionary to an array

        # Process variable id tracking variable
        pid = 0

        for array in data_array:
            pid += 1
            data = {'PROCESS_VARIABLE_ID': pid,
                    'PV_NAME': array[0],
                    'PV_DESC': array[1],
                    'PV_DEF': array[2],
                    }
            data_dictionary_array.append(data)

        user = pwd.getpwuid(os.getuid()).pw_name

        current_app.logger.info("Getting session values...")

        # Get required values from the session
        run_id = session['id']
        run_name = session['run_name']
        period = session['period']
        year = session['year']

        current_app.logger.debug("Session values: %s, %s, %s, %s, %s, %s.", run_id, run_name, period, year, user)

        # Creates a new pv set if run_id doesn't already exist, otherwise delete existing rows and repopulate
        if run_id not in app_methods.get_all_run_ids():
            current_app.logger.info("New run_id given, creating new process variable set...")

            # Creates a new set of process variables, then fill the empty set with the edited javascript data
            app_methods.create_process_variables_set(run_id, run_name, user, period, year)

            # Fill newly created pv set with new process variables (for new runs)
            app_methods.create_process_variables(run_id, data_dictionary_array)
            current_app.logger.info("New process variable set created.")
        else:
            current_app.logger.info("Existing run_id given, updating records...")

            # Edit existing process variables (for edit run)
            app_methods.edit_process_variables(run_id, data_dictionary_array)
            current_app.logger.info("Records updated successfully.")

        return redirect('/new_run/new_run_5/'+run_id)

    template_id = session['template_id']

    run_id = session['id']

    header = ['PV_NAME', 'PV_REASON', 'PV_CONTENT']

    records = app_methods.get_process_variables(template_id)
    builds = app_methods.get_process_variables_builds(template_id)
    variables = app_methods.get_process_variables_variables()
    return render_template('new_run_4.html', run_id=run_id, table=records, builds=builds,
                           header=header, pv_variables=variables)
