from itertools import permutations
import time
import uuid
import pytest_flask as pyflk
from ips.services.new_run_steps.step_5 import run_step_5
from ips.services.forms import LoadDataForm
import ips.services.new_run as new_runner
from ips.util.ui_logging import log
import pytest

from io import BytesIO

from unittest import mock
from flask import render_template

from flask import json
from flask import request, Flask, current_app
from wtforms import FileField
from wtforms import HiddenField
from wtforms import IntegerField
from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms.widgets import HiddenInput
from flask_wtf.file import FileField, FileRequired
from flask_wtf import FlaskForm
from ips import app as ips_app
from flask_login import login_user
from ips.services.models import User

start_time = time.time()
run_id = str(uuid.uuid4())

# noinspection PyUnusedLocal
def setup_module(module):
    log.info("Module level start time: {}".format(start_time))

@pytest.mark.parametrize(
    "survey_filename",
    ["survey_data.csv", ""],
    ids=["survey-filename", "no-survey-filename"]
)
@pytest.mark.parametrize(
    "shift_filename",
    ["shift_data.csv", ""],
    ids=["shift-filename", "no-shift-filename"]
)
@pytest.mark.parametrize(
    "nr_filename",
    ["nr_data.csv", ""],
    ids=["nr-filename", "no-nr-filename"]
)
@pytest.mark.parametrize(
    "unsampled_filename",
    ["unsampled_data.csv", ""],
    ids=["unsampled-filename", "no-unsampled-filename"]
)
@pytest.mark.parametrize(
    "tunnel_filename",
    ["tunnel_data.csv", ""],
    ids=["tunnel-filename", "no-tunnel-filename"]
)
@pytest.mark.parametrize(
    "sea_filename",
    ["sea_data.csv", ""],
    ids=["sea-filename", "no-sea-filename"]
)
@pytest.mark.parametrize(
    "air_filename",
    ["air_data.csv", ""],
    ids=["air-filename", "no-air-filename"]
)
def test_dynamic_form_validators(survey_filename, shift_filename, nr_filename, unsampled_filename, tunnel_filename, sea_filename, air_filename, app, client):
    """
    Tests if filename is supplied for a field then no FileRequired validator is applie
  """
    @app.route("/", methods=["POST"])
    def index():

        loadform = LoadDataForm(
            meta={
                'survey_file': survey_filename,
                'shift_file': shift_filename,
                'non_response_file': nr_filename,
                'unsampled_file': unsampled_filename,
                'tunnel_file': tunnel_filename,
                'sea_file': sea_filename,
                'air_file': air_filename}
        )
        loadform.validate()

        file_fields = [
            "survey_file", "non_response_file", "unsampled_file", "tunnel_file", "sea_file",
            "air_file", "shift_file"
        ]
        for field in file_fields:
            if getattr(loadform.meta, field):
                assert field not in loadform._extra_validators, f"Extra validator not expected if {field} filename supplied"
                assert field not in loadform.errors
            else:
                assert field in loadform._extra_validators, f"Extra validator expected if {field} filename supplied"
                assert any([
                    isinstance(validator, FileRequired) for validator in loadform._extra_validators[field]
                ]) is True, f"FileRequired validator expected as extra validator when no filename supplied for {field}"
                assert loadform.errors[field] == ['This field is required.'], f"Expected {field} field validation to fail as no filename givened"
    client.post("/")

@mock.patch('ips.services.new_run_steps.step_5.render_template')
@mock.patch('ips.services.new_run_steps.step_5.app_methods')
def test_file_upload_view_uploads_required_files(mock_app_methods, mock_render_template):
    """
    Tests that every file upload is attempted, even if there are any errors in other files.
    """ 
    ips_app.config['WTF_CSRF_ENABLED'] = False # ensure CSRF protection off when we post the form

    client = ips_app.test_client()

    # Login test client by calling login view
    with mock.patch("ips.services.auth.requests") as mock_requests:
        mock_requests.get.return_value.status_code = 200
        resp = client.post(
            "/login",
            data={
                "username": "dummy-username",
                "password": "dummy-password"
            },
            follow_redirects=False
        )

    mock_app_methods.get_run.return_value = {
        'SURVEY_FILE': '',
        'SHIFT_FILE': '',
        'NR_FILE': '',
        'UNSAMPLED_FILE': '',
        'TUNNEL_FILE': '',
        'SEA_FILE': '',
        'AIR_FILE': ''
    }
    mock_app_methods.import_data.return_value.status_code = 400
    mock_app_methods.get_error_message.side_effect = lambda rsp, file_type: f"Invalid {file_type} data"
    mock_render_template.return_value = "Dummy Response" 
    
    # Add session keys expected by calls to import_data within step_5 view function
    with client.session_transaction() as sess:
        sess['id'] = '12345'
        sess['period'] = '05'
        sess['year'] = '2017'

    test_user = User('Mr Anonymous')
    with ips_app.app_context():
        with ips_app.test_request_context():
            login_user(test_user)

    file_data = BytesIO(b"abcdef")
    resp = client.post(
        "/new_run_steps/new_run_5/abc-123-def",
        content_type="multipart/form-data",
        buffered=True,
        data={
            'survey_file': (file_data, 'surveydata.csv'),
            'shift_file': (file_data, 'shift_data.csv'),
            'non_response_file': (file_data, 'nr_data.csv'),
            'unsampled_file': (file_data, 'unsampled_data.csv'),
            'tunnel_file': (file_data, 'tunnel_file.csv'),
            'sea_file': (file_data, 'sea_data.csv'),
            'air_file': (file_data, 'air_data.csv'),
        },
        follow_redirects=False
    )

    assert len(mock_app_methods.import_data.call_args_list) == 7, "Attempted to upload add file-types" 

def test_odd_empty_validation_error(app, client):
    
    """When we run the empty validation on a new run, we get the error as supposed.
    But then after that, we edit a fully loaded run, left some or all empty, and click on save and continue, THAT SAME error occurs.
    This test will attempt to create an empty run, which gives the error, then add a new filled in run to confirm."""

    @app.route("/", methods=["POST"])
    def index():

        empty_form = LoadDataForm(
            meta={
                'survey_file': '',
                'shift_file': '',
                'non_response_file': '',
                'unsampled_file': '',
                'tunnel_file': '',
                'sea_file': '',
                'air_file': ''
        })

        full_form = LoadDataForm(
            meta={
                'survey_file': 'survey_data.csv',
                'shift_file': 'shift_data.csv',
                'non_response_file': 'nr_data.csv',
                'unsampled_file': 'unsampled_data.csv',
                'tunnel_file': 'tunnel_data.csv',
                'sea_file': 'sea_data.csv',
                'air_file': 'air_data.csv'
        })

        file_fields = [
            "survey_file", "non_response_file", "unsampled_file", "tunnel_file", "sea_file",
            "air_file", "shift_file"
        ]
        for field in file_fields:
            if getattr(full_form.meta, field):
                assert field not in full_form._extra_validators, f"Extra validator not expected if {field} filename supplied"
            else:
                assert field in full_form._extra_validators, f"Extra validator expected if {field} filename supplied"
                assert any([
                    isinstance(validator, FileRequired) for validator in full_form._extra_validators[field]
                ]) is True, f"FileRequired validator expected as extra validator when no filename supplied for {field}"
    client.post("/")

    

def test_all_preloaded_success(app, client):
    @app.route("/", methods=["POST"])
    def index():
        preload_form = LoadDataForm(
            meta={
                'survey_file': 'survey_data.csv',
                'shift_file': 'shift_data.csv',
                'non_response_file': 'nr_data.csv',
                'unsampled_file': 'unsampled_data.csv',
                'tunnel_file': 'tunnel_data.csv',
                'sea_file': 'sea_data.csv',
                'air_file': 'air_data.csv'
        })

        upload_file_types = [
            "survey_file", "non_response_file", "unsampled_file", "tunnel_file", "sea_file",
            "air_file", "shift_file"
        ]
        for file_type in upload_file_types:
            if getattr(preload_form.meta, file_type):
                assert any([
                    isinstance(validator, FileRequired) for validator in preload_form.survey_file.validators
                ]) is False
            else:
                assert any([
                    isinstance(validator, FileRequired) for validator in preload_form.survey_file.validators
                ]) is True


    client.post("/")
    pass

# noinspection PyUnusedLocal
def teardown_module(module):
    log.info("Duration: {}".format(time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))))