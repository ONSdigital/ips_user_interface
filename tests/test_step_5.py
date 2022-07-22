from itertools import permutations
import time
import uuid
from ips.services.forms import LoadDataForm
import pytest_flask as pyflk
from ips.services.new_run_steps.step_5 import run_step_5
import ips.services.new_run as new_runner
import pytest
from ips.util.ui_logging import log

from io import BytesIO

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
from remote_pdb import RemotePdb

start_time = time.time()
run_id = str(uuid.uuid4())

# noinspection PyUnusedLocal
def setup_module(module):

    log.info("Module level start time: {}".format(start_time))

#@pytest.mark.options(debug=False)
def test_app(app):
    assert not app.debug, 'Ensure the app is not in debug mode'


#def test_load_data_form_validation():
#    form = LoadDataForm(meta={})
    #assert(SomeValidatorClass in form.some_field_name.validators)   
"""
These parametrize sets the file name, with the list of string and their respective ids,
applied to the test_dynamic_form_validators as parameters
"""
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
    Tests if filename is supplied for a field then no FileRequired validator is applied
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

        upload_file_types = [
            "survey_file", "non_response_file", "unsampled_file", "tunnel_file", "sea_file",
            "air_file", "shift_file"
        ]
        
        for file_type in upload_file_types:
            if getattr(loadform.meta, file_type):
                assert any([
                   isinstance(validator, FileRequired) for validator in loadform.survey_file.validators
                ]) is False, f"FileRequired validator not expected when {file_type} filename supplied" 
            else:
                assert any([
                    isinstance(validator, FileRequired) for validator in loadform.survey_file.validators
                ]) is True, f"FileRequired validator expected when no filename supplied for {file_type}"
    
    client.post("/")

def test_odd_empty_validation_error(app, client):
    
    """When we run the empty validation on a new run, we get the error as supposed.
    But then after that, we edit a fully loaded run, left some or all empty, and click on save and continue, THAT SAME error occurs.
    This test will attempt to create an empty run, which gives the error, then add a new filled in run to confirm."""

    @app.route("/", methods=["POST"])
    def index():
        RemotePdb('0.0.0.0', 4445).set_trace()
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

        upload_file_types = [
            "survey_file", "non_response_file", "unsampled_file", "tunnel_file", "sea_file",
            "air_file", "shift_file"
        ]
        #RemotePdb('0.0.0.0', 4445).set_trace()    
        for file_type in upload_file_types:
            if getattr(full_form.meta, file_type):
                assert any([
                    isinstance(validator, FileRequired) for validator in full_form.survey_file.validators
                ]) is False, f"FileRequired validator not expected when {file_type} filename supplied" 
            else:
                assert any([
                    isinstance(validator, FileRequired) for validator in full_form.survey_file.validators
                ]) is True, f"FileRequired validator expected when no filename supplied for {file_type}"


    client.post("/")

    

def test_all_preloaded_success(app, client):
    @app.route("/", methods=["POST"])
    def index():
        #breakpoint()
        #RemotePdb('0.0.0.0', 4445).set_trace()
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
        #RemotePdb('0.0.0.0', 4445).set_trace()    
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

#def test_all_preloaded_save_continue_success():
#    pass

#def test_change_preloaded_success():
#    pass

#def test_change_preloaded_save_continue_success():
#    pass


# noinspection PyUnusedLocal
def teardown_module(module):
    log.info("Duration: {}".format(time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))))