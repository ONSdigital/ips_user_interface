import csv
import io
import json
import os
import requests
from datetime import datetime
from flask import Flask, request, url_for, redirect, current_app
from werkzeug.utils import secure_filename
from ips.util.ui_configuration import UIConfiguration


APP_DIR = os.path.dirname(__file__)
API_TARGET = UIConfiguration().get_api_uri()


def create_run(unique_id, run_name, run_description, user_id, period, year, run_type='0', run_status='0'):
    """
    Purpose: Creates a new run and adds it to the current list of runs (.csv currently but will be to database).

    :return: NA
    """
    new_run = {
        'RUN_ID': unique_id,
        'RUN_NAME': run_name,
        'RUN_DESC': run_description,
        'USER_ID': user_id,
        'PERIOD': period,
        'YEAR': year,
        'RUN_TYPE_ID': run_type,
        'RUN_STATUS': run_status,
        'LAST_MODIFIED': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    requests.post(API_TARGET + r"/runs", json=new_run)

    create_run_steps(new_run['RUN_ID'])


def edit_run(run_id, run_name, run_description, period, year, run_type='0', run_status='0'):
    """
    Purpose: Modifies an already existing run through a PUT request.

    :return: NA
    """

    response = requests.get(API_TARGET + r'/runs')

    file = json.loads(response.content)
    run = file[0]

    run['RUN_ID'] = run_id
    run['RUN_NAME'] = run_name
    run['RUN_DESC'] = run_description
    run['PERIOD'] = period
    run['YEAR'] = year
    run['RUN_TYPE_ID'] = run_type
    run['RUN_STATUS'] = run_status
    run['LAST_MODIFIED'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    s = API_TARGET + r'/runs/' + run_id
    requests.put(API_TARGET + r'/runs/' + run_id, json=run)


def get_system_info():
    """
    Purpose: Collects and returns the current build's system info to be displayed on the web application.
             This function uses placeholder data and may not be required in the final system.

    :return: List of records containing the system info
    """
    import flask
    import sys
    import ips_common
    return [
        ['Technology', 'Version'],
        ['Flask', flask.__version__],
        ['Python', sys.version],
        ['IPS-Common-Library', ips_common.__version__]
    ]


def get_runs():
    """
    Purpose: Gets all of the runs to put in the list

    :return: List of JSON object runs
    """

    response = requests.get(API_TARGET + r'/runs')
    return json.loads(response.content)


def get_run(run_id):
    """
    Purpose: Gets a single run by ID

    :return: A specific JSON run object
    """
    response = requests.get(API_TARGET + r'/runs')
    runs = json.loads(response.content)

    for x in runs:
        if x['RUN_ID'] == run_id:
            return x


def get_display_data_json(table_name, run_id=None, data_source=None):
    column_sets = {
        'SHIFT_DATA': [
            'PORTROUTE', 'WEEKDAY', 'ARRIVEDEPART', 'AM_PM_NIGHT', 'TOTAL'
        ],
        'TRAFFIC_DATA': [
            'PORTROUTE', 'PERIODSTART', 'PERIODEND', 'ARRIVEDEPART', 'AM_PM_NIGHT',
            'TRAFFICTOTAL', 'HAUL'
        ],
        'NON_RESPONSE_DATA': [
            'PORTROUTE', 'WEEKDAY', 'ARRIVEDEPART', 'AM_PM_NIGHT', 'SAMPINTERVAL',
            'MIGTOTAL', 'ORDTOTAL'
        ],
        'UNSAMPLED_OOH_DATA': [
            'PORTROUTE', 'REGION', 'ARRIVEDEPART', 'UNSAMP_TOTAL'
        ],
        'PS_SHIFT_DATA': [
            'SHIFT_PORT_GRP_PV', 'ARRIVEDEPART', 'WEEKDAY_END_PV', 'AM_PM_NIGHT_PV', 'MIGSI',
            'POSS_SHIFT_CROSS', 'SAMP_SHIFT_CROSS', 'MIN_SH_WT', 'MEAN_SH_WT', 'MAX_SH_WT',
            'COUNT_RESPS', 'SUM_SH_WT'
        ],
        'PS_NON_RESPONSE': [
            'NR_PORT_GRP_PV', 'ARRIVEDEPART', 'WEEKDAY_END_PV', 'MEAN_RESPS_SH_WT',
            'COUNT_RESPS',
            'PRIOR_SUM', 'GROSS_RESP', 'GNR', 'MEAN_NR_WT'
        ],
        'PS_MINIMUMS': [
            'MINS_PORT_GRP_PV', 'ARRIVEDEPART', 'MINS_CTRY_GRP_PV', 'MINS_NAT_GRP_PV',
            'MINS_NAT_GRP_PV',
            'MINS_CTRY_PORT_GRP_PV', 'MINS_CASES', 'FULLS_CASES', 'PRIOR_GROSS_MINS',
            'PRIOR_GROSS_FULLS',
            'PRIOR_GROSS_ALL', 'MINS_WT', 'POST_SUM', 'CASES_CARRIED_FWD'
        ],
        'PS_TRAFFIC': [
            'SAMP_PORT_GRP_PV', 'ARRIVEDEPART', 'FOOT_OR_VEHICLE_PV', 'CASES', 'TRAFFICTOTAL',
            'SUM_TRAFFIC_WT', 'TRAFFIC_WT'
        ],
        'PS_UNSAMPLED_OOH': [
            'UNSAMP_PORT_GRP_PV', 'ARRIVEDEPART', 'UNSAMP_REGION_GRP_PV', 'CASES',
            'SUM_PRIOR_WT',
            'SUM_UNSAMP_TRAFFIC_WT', 'UNSAMP_TRAFFIC_WT'
        ],
        'PS_IMBALANCE': [
            'FLOW', 'SUM_PRIOR_WT', 'SUM_IMBAL_WT'
        ],
        'PS_FINAL': [
            'SERIAL', 'SHIFT_WT', 'NON_RESPONSE_WT', 'MINS_WT', 'TRAFFIC_WT',
            'UNSAMP_TRAFFIC_WT', 'IMBAL_WT', 'FINAL_WT'
        ]
    }


def get_process_variables(run_id):
    response = requests.get(API_TARGET + r'/process_variables/TEMPLATE')

    return json.loads(response.content)


def get_process_variables_builds(run_id):
    response = requests.get(API_TARGET + r'/builder/' + run_id)
    return json.loads(response.content)


def get_process_variables_variables():
    response = requests.get(API_TARGET + r'/builder/variables')
    return json.loads(response.content)


def create_process_variables_set(run_id, name, user, period, year):
    response = requests.get(API_TARGET + r'/pv_sets')
    file = json.loads(response.content)
    new_pv_set = file[0]

    new_pv_set['RUN_ID'] = run_id
    new_pv_set['NAME'] = name
    new_pv_set['USER'] = user
    new_pv_set['PERIOD'] = period
    new_pv_set['YEAR'] = year

    requests.post(API_TARGET + r'/pv_sets', json=new_pv_set)


def create_process_variables(run_id, json):
    requests.post(API_TARGET + r'/process_variables/' + run_id, json=json)


def get_process_variable_sets():
    response = requests.get(API_TARGET + r'/pv_sets')
    return json.loads(response.content)


def create_run_steps(run_id):
    """
    Purpose: Creates a new set of run steps for a newly generated run.

    :return: NA
    """
    route = API_TARGET + r"/run_steps/" + run_id

    requests.post(route)


def get_run_steps(run_id):
    address = API_TARGET + r'/run_steps/' + run_id

    response = requests.get(address)

    if response.status_code == 200:
        values = json.loads(response.content)
    else:
        values = []

    return values


def get_export_data_table(run_id):
    """
        Purpose: Gets the export data for all the runs

        :return: List of exports as JSON
        """
    # API gateway response is a list of JSON data containing the export data for all the runs
    response = requests.get(API_TARGET + r'/EXPORT_DATA_DOWNLOAD/' + run_id)

    # Set boolean to assume records exist
    exports = 1

    # Empty data if no response
    if response.status_code == 400:
        data = [
            {
                'DATE_CREATED': '',
                'DOWNLOADABLE_DATA': '',
                'FILENAME': '',
                'RUN_ID': '',
                'SOURCE_TABLE': ''
            }
        ]
        # Set boolean if no records exist
        exports = 0
        return data, exports

    # Convert response to JSON
    json_data = json.loads(response.content)

    return json_data, exports


def export_clob(run_id, target_filename, sql_table):
    """
        Purpose: Puts the export downloadable data into a text file

        :return: NA
        """
    # API gateway response to get a single export from run id, filename and the SQL table
    response = requests.get(
        API_TARGET + r'/EXPORT_DATA_DOWNLOAD' + r'/' + run_id + r'/' + target_filename + r'/' + sql_table)

    # Convert data to json
    table_data_json = json.loads(response.content)

    # Get the downloadable data
    run = table_data_json[0]['DOWNLOADABLE_DATA']

    # Put the data in a text file saved in the project root directory with prefix .csv
    with open(target_filename + ".csv", "w") as text_file:
        print(run, file=text_file)


def create_export_data_download(run_id, sql_table):
    """
            Purpose: Gets the export data and puts into a single long string
            :return: Boolean - posts the data to the database
            """

    # Get the export data by SQL table and run id
    try:
        response = requests.get(API_TARGET + r'/export/' + run_id + r'/' + sql_table)
        # Convert to JSON
        table_data_json = json.loads(response.content)
        return table_data_json['DOWNLOADABLE_DATA']
    except Exception as err:
        return False


def edit_process_variables(run_id, json_dictionary):
    """
    :param run_id:
    :param pv_content:
    :param pv_name:
    :param reason_for_change:
    :return:
    """
    response = requests.delete(API_TARGET + r'/process_variables/' + run_id)

    create_process_variables(run_id, json_dictionary)


def import_data(table_name, run_id, file, month=None, year=None):
    return requests.post(f"{API_TARGET}/import/{table_name}/{run_id}",
                         files={'ips-file': file},
                         data={'month': month, 'year': year})


#George left this here as we may well use it at some point.
def delete_data(table_name, run_id=None):
    route = API_TARGET + r'/' + table_name

    if run_id:
        route = route + r'/' + run_id

    rv = requests.delete(route)
    print("DELETE - " + table_name)
    print(rv)


# TODO: El needs this to refactor and move validation to ips_services and can then be removed
def date_check(month, year, month_list, year_list):
    date_error = False
    month = [month]
    year = [year]

    if month[0][0] == 'Q':
        quarter = month[0][1]
        if quarter == '1':
            month = ['1', '2', '3']
        elif quarter == '2':
            month = ['4', '5', '6']
        elif quarter == '3':
            month = ['7', '8', '9']
        elif quarter == '4':
            month = ['10', '11', '12']
    if not all(elem in month for elem in month_list):
        date_error = True
    elif not all(elem in year for elem in year_list):
        date_error = True
    return date_error


# TODO: El needs this to refactor and move validation to ips_services and can then be removed
def survey_data_import(import_data_file, month, year):
    # Import  data
    stream = io.StringIO(import_data_file.stream.read().decode("utf-8"), newline=None)
    import_csv = csv.DictReader(stream)
    import_csv.fieldnames = [name.upper() for name in import_csv.fieldnames]

    month_set = set([])
    year_set = set([])
    for row in import_csv:
        month_set.add(row['INTDATE'][-6:][:2])
        year_set.add(row['INTDATE'][-4:])

    month_list = list(month_set)
    year_list = list(year_set)
    date_error = date_check(month, year, month_list, year_list)

    print("Field Names:")
    print(import_csv.fieldnames)

    serial_error = False
    # column_error = False

    if import_csv.fieldnames[0] != "SERIAL":
        # if the serial column is invalid
        serial_error = True

    return serial_error, date_error


def get_run_step_requests(run_id, step_number=None):
    address = API_TARGET + r'/RESPONSE/' + run_id

    if step_number:
        address = address + r'/' + step_number

    response = requests.get(address)

    if response.status_code == 200:
        values = json.loads(response.content)
    else:
        values = []

    return values


# Steps to run comes through as a string list containing the step numbers to run
def start_run(run_id):
    requests.put(API_TARGET + r'/ips-service/start/' + str(run_id))


def cancel_run(run_id):
    requests.get(API_TARGET + r'/ips-service/cancel/' + str(run_id))


def get_all_run_ids():
    response = requests.get(API_TARGET + r'/pv_sets')
    dictionary_of_pv_sets = json.loads(response.content)

    list_of_run_ids = []

    for record in dictionary_of_pv_sets:
        list_of_run_ids.append(record['RUN_ID'])

    return list_of_run_ids


def getErrorMessage(resp):
    resp = json.loads(resp.content.decode('utf-8'))
    resp = resp['description']
    s = resp.find('(') + 1
    resp = resp[s:-1]
    error_message = resp.split(',')[2]
    return error_message
