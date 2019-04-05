from ips.forms import DataSelectionForm, LoadDataForm
import pytest
import ips as web
from werkzeug.datastructures import FileStorage

app = web.create_app()

@pytest.fixture()
def client():
    """The flask test client for our app.

    This lets us trigger http requests to end points without needing a server running.
    """

    app.testing = True
    app.config["WTF_CSRF_ENABLED"] = False
    client = app.test_client()


    return client


class TestNewRun1:

    # GETS

    # No Run ID (New)
    def test_get_webpage_no_run_id_returns_ok(self, client):

        res = client.get('/new_run/new_run_1')
        assert res.status_code == 200

    def test_get_webpage_no_run_id_renders_correct_info_banner(self, client):
        res = client.get('/new_run/new_run_1')
        assert b'You are creating a new IPS run.' in res.data

    def test_get_webpage_no_run_id_renders_page_title(self, client):
        res = client.get('/new_run/new_run_1')
        assert b'Run details' in res.data

    def test_get_webpage_no_run_id_renders_step_indicator(self, client):
        res = client.get('/new_run/new_run_1')
        assert b'Step 1' in res.data

    def test_get_webpage_no_run_id_renders_run_name_label(self, client):
        res = client.get('/new_run/new_run_1')
        assert b'Name' in res.data

    def test_get_webpage_no_run_id_renders_run_description_label(self, client):
        res = client.get('/new_run/new_run_1')
        assert b'Description' in res.data

    def test_get_webpage_no_run_id_renders_save_and_continue_button(self, client):
        res = client.get('/new_run/new_run_1')
        assert b'Save and continue' in res.data

    def test_get_webpage_no_run_id_renders_cancel_button(self, client):
        res = client.get('/new_run/new_run_1')
        assert b'Cancel' in res.data

    # Valid Run ID (Edit)
    def test_get_webpage_valid_run_id_returns_ok(self, client):

        res = client.get('/new_run/new_run_1/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert res.status_code == 200

    def test_get_webpage_valid_run_id_renders_correct_info_banner(self, client):
        res = client.get('/new_run/new_run_1/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'You are editing run: 9e5c1872-3f8e-4ae5-85dc-c67a602d011e' in res.data

    def test_get_webpage_valid_run_id_renders_page_title(self, client):
        res = client.get('/new_run/new_run_1/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'Run details' in res.data

    def test_get_webpage_valid_run_id_renders_step_indicator(self, client):
        res = client.get('/new_run/new_run_1/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'Step 1' in res.data

    def test_get_webpage_valid_run_id_renders_run_name_label(self, client):
        res = client.get('/new_run/new_run_1/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'Name' in res.data

    def test_get_webpage_valid_run_id_renders_run_description_label(self, client):
        res = client.get('/new_run/new_run_1/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'Description' in res.data

    def test_get_webpage_valid_run_id_renders_save_and_continue_button(self, client):
        res = client.get('/new_run/new_run_1/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'Save and continue' in res.data

    def test_get_webpage_valid_run_id_renders_cancel_button(self, client):
        res = client.get('/new_run/new_run_1/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'Cancel' in res.data

    # POSTS

    # Save and continue button
    def test_pressing_save_and_continue_button_with_no_form_data_returns_ok(self, client):

        with app.test_request_context():
            # Post to page with  no form data
            res = client.post('/new_run/new_run_1')

        assert res.status_code == 200

    def test_pressing_save_and_continue_button_with_no_form_data_triggers_validation_errors(self, client):
        with app.test_request_context():
            # Post to page with no form data
            res = client.post('/new_run/new_run_1')

        # Ensure validation failed
        assert b'This field is required.' in res.data


class TestNewRun2:
    # GETS

    # No Run ID (New)
    def test_get_webpage_no_run_id_returns_ok(self, client):
        res = client.get('/new_run/new_run_2')
        assert res.status_code == 200

    def test_get_webpage_no_run_id_renders_correct_info_banner(self, client):
        res = client.get('/new_run/new_run_2')
        assert b'You are creating a new IPS run.' in res.data

    def test_get_webpage_no_run_id_renders_page_title(self, client):
        res = client.get('/new_run/new_run_2')
        assert b'Select fieldwork' in res.data

    def test_get_webpage_no_run_id_renders_step_indicator(self, client):
        res = client.get('/new_run/new_run_2')
        assert b'Step 2' in res.data

    def test_get_webpage_no_run_id_renders_start_date_label(self, client):
        res = client.get('/new_run/new_run_2')
        assert b'Start date' in res.data

    def test_get_webpage_no_run_id_renders_run_description_label(self, client):
        res = client.get('/new_run/new_run_2')
        assert b'End date' in res.data

    def test_get_webpage_no_run_id_renders_day_label(self, client):
        res = client.get('/new_run/new_run_2')
        assert b'Day' in res.data

    def test_get_webpage_no_run_id_renders_month_label(self, client):
        res = client.get('/new_run/new_run_2')
        assert b'Month' in res.data

    def test_get_webpage_no_run_id_renders_year_label(self, client):
        res = client.get('/new_run/new_run_2')
        assert b'Year' in res.data

    def test_get_webpage_no_run_id_renders_save_and_continue_button(self, client):
        res = client.get('/new_run/new_run_2')
        assert b'Save and continue' in res.data

    def test_get_webpage_no_run_id_renders_back_button(self, client):
        res = client.get('/new_run/new_run_2')
        assert b'Back' in res.data

    def test_get_webpage_no_run_id_renders_cancel_button(self, client):
        res = client.get('/new_run/new_run_2')
        assert b'Cancel' in res.data

    # Valid Run ID (Edit)
    def test_get_webpage_valid_run_id_returns_ok(self, client):
        res = client.get('/new_run/new_run_2/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert res.status_code == 200

    def test_get_webpage_valid_run_id_renders_correct_info_banner(self, client):
        res = client.get('/new_run/new_run_2/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'You are editing run: 9e5c1872-3f8e-4ae5-85dc-c67a602d011e' in res.data

    def test_get_webpage_valid_run_id_renders_page_title(self, client):
        res = client.get('/new_run/new_run_2/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'Select fieldwork' in res.data

    def test_get_webpage_valid_run_id_renders_step_indicator(self, client):
        res = client.get('/new_run/new_run_2/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'Step 2' in res.data

    def test_get_webpage_valid_run_id_renders_start_date_label(self, client):
        res = client.get('/new_run/new_run_2/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'Start date' in res.data

    def test_get_webpage_valid_run_id_renders_run_description_label(self, client):
        res = client.get('/new_run/new_run_2/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'End date' in res.data

    def test_get_webpage_valid_run_id_renders_day_label(self, client):
        res = client.get('/new_run/new_run_2/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'Day' in res.data

    def test_get_webpage_valid_run_id_renders_month_label(self, client):
        res = client.get('/new_run/new_run_2/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'Month' in res.data

    def test_get_webpage_valid_run_id_renders_year_label(self, client):
        res = client.get('/new_run/new_run_2/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'Year' in res.data

    def test_get_webpage_valid_run_id_renders_save_and_continue_button(self, client):
        res = client.get('/new_run/new_run_2/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'Save and continue' in res.data

    def test_get_webpage_valid_run_id_renders_back_button(self, client):
        res = client.get('/new_run/new_run_2/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'Back' in res.data

    def test_get_webpage_valid_run_id_renders_cancel_button(self, client):
        res = client.get('/new_run/new_run_2/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'Cancel' in res.data


class TestNewRun3:
    # GETS

    # No Run ID (New)
    def test_get_webpage_no_run_id_returns_ok(self, client):
        res = client.get('/new_run/new_run_3')
        assert res.status_code == 200

    def test_get_webpage_no_run_id_renders_page_title(self, client):
        res = client.get('/new_run/new_run_3')
        assert b'Load data' in res.data

    def test_get_webpage_no_run_id_renders_step_indicator(self, client):
        res = client.get('/new_run/new_run_3')
        assert b'Step 3' in res.data

    def test_get_webpage_no_run_id_renders_survey_data_label(self, client):
        res = client.get('/new_run/new_run_3')
        assert b'Survey data' in res.data

    def test_get_webpage_no_run_id_renders_external_data_label(self, client):
        res = client.get('/new_run/new_run_3')
        assert b'External data' in res.data

    def test_get_webpage_no_run_id_renders_day_label(self, client):
        res = client.get('/new_run/new_run_3')
        assert b'Shift data' in res.data

    def test_get_webpage_no_run_id_renders_month_label(self, client):
        res = client.get('/new_run/new_run_3')
        assert b'Non_response data' in res.data

    def test_get_webpage_no_run_id_renders_year_label(self, client):
        res = client.get('/new_run/new_run_3')
        assert b'Unsampled data' in res.data

    def test_get_webpage_no_run_id_renders_day_label(self, client):
        res = client.get('/new_run/new_run_3')
        assert b'Tunnel data' in res.data

    def test_get_webpage_no_run_id_renders_month_label(self, client):
        res = client.get('/new_run/new_run_3')
        assert b'Sea data' in res.data

    def test_get_webpage_no_run_id_renders_year_label(self, client):
        res = client.get('/new_run/new_run_3')
        assert b'Air data' in res.data

    def test_get_webpage_no_run_id_renders_save_and_continue_button(self, client):
        res = client.get('/new_run/new_run_3')
        assert b'Save and continue' in res.data

    def test_get_webpage_no_run_id_renders_back_button(self, client):
        res = client.get('/new_run/new_run_3')
        assert b'Back' in res.data

    def test_get_webpage_no_run_id_renders_cancel_button(self, client):
        res = client.get('/new_run/new_run_3')
        assert b'Cancel' in res.data

    # Test that the standard page renders correctly.
    def test_get_webpage_no_run_id_renders_file_type_message(self, client):
        res = client.get('/new_run/new_run_3')
        assert b'File type accepted is .csv' in res.data

    # Test that no error messages display when first seeing the basic page.
    def test_get_webpage_no_run_id_renders_no_errors_when_first_loaded(self, client):
        res = client.get('/new_run/new_run_3')
        assert b'This field is required.' not in res.data
        assert b'All fields must be filled with .csv files only.' not in res.data

    # Valid Run ID (Edit)
    def test_get_webpage_valid_run_id_returns_ok(self, client):
        res = client.get('/new_run/new_run_3/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert res.status_code == 200

    def test_get_webpage_valid_run_id_renders_page_title(self, client):
        res = client.get('/new_run/new_run_3/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'Load data' in res.data

    def test_get_webpage_valid_run_id_renders_step_indicator(self, client):
        res = client.get('/new_run/new_run_3/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'Step 3' in res.data

    def test_get_webpage_valid_run_id_renders_survey_data_label(self, client):
        res = client.get('/new_run/new_run_3/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'Survey data' in res.data

    def test_get_webpage_valid_run_id_renders_external_data_label(self, client):
        res = client.get('/new_run/new_run_3/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'External data' in res.data

    def test_get_webpage_valid_run_id_renders_day_label(self, client):
        res = client.get('/new_run/new_run_3/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'Shift data' in res.data

    def test_get_webpage_valid_run_id_renders_month_label(self, client):
        res = client.get('/new_run/new_run_3/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'Non_response data' in res.data

    def test_get_webpage_valid_run_id_renders_year_label(self, client):
        res = client.get('/new_run/new_run_3/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'Unsampled data' in res.data

    def test_get_webpage_valid_run_id_renders_day_label(self, client):
        res = client.get('/new_run/new_run_3/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'Tunnel data' in res.data

    def test_get_webpage_valid_run_id_renders_month_label(self, client):
        res = client.get('/new_run/new_run_3/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'Sea data' in res.data

    def test_get_webpage_valid_run_id_renders_year_label(self, client):
        res = client.get('/new_run/new_run_3/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'Air data' in res.data

    def test_get_webpage_valid_run_id_renders_save_and_continue_button(self, client):
        res = client.get('/new_run/new_run_3/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'Save and continue' in res.data

    def test_get_webpage_valid_run_id_renders_back_button(self, client):
        res = client.get('/new_run/new_run_3/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'Back' in res.data

    def test_get_webpage_valid_run_id_renders_cancel_button(self, client):
        res = client.get('/new_run/new_run_3/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'Cancel' in res.data

    # Test that the standard page renders correctly.
    def test_get_webpage_valid_run_id_renders_file_type_message(self, client):
        res = client.get('/new_run/new_run_3/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'File type accepted is .csv' in res.data

    # Test that no error messages display when first seeing the basic page.
    def test_get_webpage_valid_run_id_renders_no_errors_when_first_loaded(self, client):
        res = client.get('/new_run/new_run_3/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'This field is required.' not in res.data
        assert b'All fields must be filled with .csv files only.' not in res.data

    # POSTS

    # No Run ID (New)

    # TODO: ensure that the test gives the expected number of these error messages
    # Test that an error is displayed if no files are given.
    def test_webpage_no_run_id_renders_errors_when_missing_information(self, client):
        res = client.post('/new_run/new_run_3')
        assert b'This field is required.' in res.data

    # Valid Run ID (Edit)

    # TODO: ensure that the test gives the expected number of these error messages
    # Test that an error is displayed if no files are given.
    def test_webpage_valid_run_id_renders_errors_when_missing_information(self, client):
        res = client.post('/new_run/new_run_3/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert b'This field is required.' in res.data

    # Test that an error is displayed if no files are given.
    @pytest.mark.skip
    def test_missing_files_error_new_run_3(self, client):
        res = client.post('/new_run/new_run_3')
        assert res.status_code == 200
        assert b'This field is required.' in res.data

    @pytest.mark.skip
    def test_wrong_files_error_new_run_3(self, client):
        with app.test_request_context():
            dummy_file = FileStorage(filename='data.txt')
            form = LoadDataForm(survey_file=dummy_file,
                                shift_file=dummy_file,
                                non_response_file=dummy_file,
                                unsampled_file=dummy_file,
                                tunnel_file=dummy_file,
                                sea_file=dummy_file,
                                air_file=dummy_file)

            res = client.post('/new_run/new_run_3', data=form.data, follow_redirects=True)
        assert res.status_code == 200
        assert b'This field is required.' in res.data
        assert b'Select process variables' not in res.data

    # Test that the error is not displayed if all files are given.
    @pytest.mark.skip
    def test_no_error_new_run_3_files(self, client):
        with app.test_request_context():
            dummy_file = FileStorage(filename='data.csv')
            form = LoadDataForm(survey_file=dummy_file,
                                shift_file=dummy_file,
                                non_response_file=dummy_file,
                                unsampled_file=dummy_file,
                                tunnel_file=dummy_file,
                                sea_file=dummy_file,
                                air_file=dummy_file)

            res = client.post('/new_run/new_run_3', data=form.data, follow_redirects=True)
        assert res.status_code == 200
        assert b'Select process variables' in res.data
        res = client.post('/new_run/new_run_3', data=new_form.data, follow_redirects=True)

        assert res.status_code == 200
        assert b'File must be a .csv file.' in res.data


class TestNewRun4:

    def test_get_webpage_renders_back_button(self, client):
        res = client.get('/new_run/new_run_4')
        assert b'Back' in res.data

    # Test that the standard page renders correctly.
    def test_default_page_new_run_4_renders_correctly_with_expected_text_from_get_request(self, client):
        res = client.get('/new_run/new_run_4')
        assert res.status_code == 200
        assert b'Select process variables set' in res.data

    # Test that the standard page renders correctly and gets the TEMPLATE pv_set from the database.
    def test_default_page_new_run_4_has_template_pv_set_included_in_the_list(self, client):
        res = client.get('/new_run/new_run_4')
        assert res.status_code == 200
        assert b'TEMPLATE' in res.data

    # Test that the standard page renders correctly.
    def test_default_page_new_run_4_renders_correctly_with_correct_headers(self, client):
        res = client.get('/new_run/new_run_4')
        assert res.status_code == 200
        assert b'Run id' and b'Name' and b'User' and b'Start Date' and b'End Date' and b'Select' in res.data

    # Test that pressing save and continue on this page will successfully navigate to the next page with no other input).
    def test_new_run_4_will_continue_onto_new_run_5_with_a_post_and_a_value_given_for_the_selected_template_id(self, client):

        with app.test_request_context():

            res = client.post('/new_run/new_run_4', data = {'selected' : 'TEMPLATE'}, follow_redirects=True)
            assert b'Edit' in res.data

    # Tests that the request does not move onwards if a template id is not given. This should never happen as it is
    # selected by default when the page is accessed by a normal request i.e. in a non-testing context
    def test_new_run_4_will_not_continue_if_a_value_is_not_given_for_the_selected_template_id(self, client):

        with app.test_request_context():

            res = client.post('/new_run/new_run_4')
            assert res.status_code == 400


class TestNewRun5:

    def test_get_webpage_renders_back_button(self, client):
        with app.test_request_context():
            with client.session_transaction() as session:
                session['template_id'] = 'TEMPLATE'
            res = client.get('/new_run/new_run_5', data={'template_id': 'TEMPLATE'})
            assert b'Back' in res.data

    def test_that_default_page_renders_correctly(self, client):

        with app.test_request_context():
            with client.session_transaction() as session:
                session['template_id'] = 'TEMPLATE'
            res = client.get('/new_run/new_run_5', data={'template_id': 'TEMPLATE'})
            assert b'Edit' in res.data

    def test_that_all_headers_render_correctly_with_get_request(self, client):
        with app.test_request_context():
            with client.session_transaction() as session:
                session['template_id'] = 'TEMPLATE'
            res = client.get('/new_run/new_run_5', data={'template_id': 'TEMPLATE'})
            assert b'PV name' and b'PV Reason' and b'Edit' in res.data

    def test_that_the_standard_header_banner_renders_correctly(self, client):
        with app.test_request_context():
            with client.session_transaction() as session:
                session['template_id'] = 'TEMPLATE'
            res = client.get('/new_run/new_run_5', data={'template_id': 'TEMPLATE'})
            assert b'Dashboard' and b'New run' and b'System info' in res.data
