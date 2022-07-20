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

def test_dynamic_form_validators(app, client):
    """
    Tests if filename is supplied for a field then no FileRequired validator is applied
    """
    @app.route("/", methods=["POST"])
    def index():
        loadform = LoadDataForm(
            meta={
                'survey_file': 'surveydata.csv',
                'shift_file': 'Poss shifts Dec 2017.csv',
                'non_response_file': 'Dec17_NR.csv',
                'unsampled_file': 'Unsampled Traffic Dec 2017 - Copy.csv',
                'tunnel_file': 'Tunnel Traffic Dec 2017.csv',
                'sea_file': 'Sea Traffic Dec 2017.csv',
                'air_file': 'Air Sheet Dec 2017 VBA.csv'}
        )

        upload_file_types = [
            "survey_file", "non_response_file", "unsampled_file", "tunnel_file", "sea_file",
            "air_file", "shift_file"
        ]
        
        for file_type in upload_file_types:
            if loadform.meta.getattr(file_type):
                assert any([
                    isinstance(validator, FileRequired) for validator in loadform.survey_file.validators
                ]) is False 
            else:
                assert any([
                    isinstance(validator, FileRequired) for validator in loadform.survey_file.validators
                ]) is True
    

def test_none_form_validators(app, client):
    """
    Tests if filename is supplied for a field then no FileRequired validator is applied
    """
    @app.route("/", methods=["POST"])
    def index():
        loadform = LoadDataForm(
            meta={
                'survey_file': '',
                'shift_file': '',
                'non_response_file': '',
                'unsampled_file': '',
                'tunnel_file': '',
                'sea_file': '',
                'air_file': ''}
        )

        upload_file_types = [
            "survey_file", "non_response_file", "unsampled_file", "tunnel_file", "sea_file",
            "air_file", "shift_file"
        ]
        
        for file_type in upload_file_types:
            if loadform.meta.getattr(file_type):
                assert all([
                    isinstance(validator, FileRequired) for validator in loadform.survey_file.validators
                ]) is False 
            else:
                assert all([
                    isinstance(validator, FileRequired) for validator in loadform.survey_file.validators
                ]) is True

def test_fully_loaded_success():
    pass
    d = run_step_5(run_id)
    assert d.form.meta.survey_file and d.form.meta.air_file and d.form.meta.nr_file and d.form.meta.tunnel_file and d.form.meta.shift_file and d.form.meta.sea_file and d.form.meta.unsampled_file


def test_all_preloaded_success():
    d = run_step_5(run_id)
    assert d.form.meta.survey_file and d.form.meta.air_file and d.form.meta.nr_file and d.form.meta.tunnel_file and d.form.meta.shift_file and d.form.meta.sea_file and d.form.meta.unsampled_file
    pass

def test_all_preloaded_save_continue_success():
    pass

def test_change_preloaded_success():
    pass

def test_change_preloaded_save_continue_success():
    pass


# noinspection PyUnusedLocal
def teardown_module(module):
    log.info("Duration: {}".format(time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))))