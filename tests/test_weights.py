from ips.forms import DataSelectionForm
import pytest
import ips as web

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


class TestDisplayWeights1:

    # GETS
    def test_get_webpage_with_no_run_id(self, client):

        res = client.get('/manage_run/weights')
        assert res.status_code == 404

    def test_get_webpage_using_valid_run_id(self, client):

        res = client.get('/manage_run/weights/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert res.status_code == 200
        assert b'9e5c1872-3f8e-4ae5-85dc-c67a602d011e' in res.data

    def test_get_webpage_using_invalid_run_id(self, client):

        res = client.get('/manage_run/weights/0000')
        assert res.status_code == 404
        assert b'Not Found' in res.data

    # POSTS

    # Shift Data Selection

    def test_selecting_shift_data_triggers_redirect(self, client):

        with app.test_request_context():
            # Setup form submission information
            form = DataSelectionForm(data_selection='SHIFT_DATA|Shift Data|0')
            # Post to weights with valid form data
            res = client.post('/manage_run/weights/9e5c1872-3f8e-4ae5-85dc-c67a602d011e', data=form.data)

        # Ensure redirect target found
        assert res.status_code == 302
        # Ensure redirecting
        assert b'Redirecting' in res.data

    def test_selecting_shift_data_gets_correct_target_page(self, client):

        with app.test_request_context():
            # Setup form submission information
            form = DataSelectionForm(data_selection='SHIFT_DATA|Shift Data|0')
            # Post to weights with valid form data
            res = client.post('/manage_run/weights/9e5c1872-3f8e-4ae5-85dc-c67a602d011e', data=form.data)

        # Ensure target is weights_2
        assert b'/weights_2' in res.data

    def test_selecting_shift_data_triggers_no_validation_errors(self, client):

        with app.test_request_context():
            # Setup form submission information
            form = DataSelectionForm(data_selection='SHIFT_DATA|Shift Data|0')
            # Post to weights with valid form data
            res = client.post('/manage_run/weights/9e5c1872-3f8e-4ae5-85dc-c67a602d011e', data=form.data)

        # Ensure validation passed
        assert b'This field is required.' not in res.data

    # No Selection

    def test_selecting_nothing_triggers_validation_errors(self, client):

        with app.test_request_context():
            # Setup form submission information
            form = DataSelectionForm(data_selection='')
            # Post to weights with invalid form data
            res = client.post('/manage_run/weights/9e5c1872-3f8e-4ae5-85dc-c67a602d011e', data=form.data)

        # Ensure status_code is 200 (OK)
        assert res.status_code == 200
        # Ensure called ID still in res data
        assert b'9e5c1872-3f8e-4ae5-85dc-c67a602d011e' in res.data
        # Ensure validation failed
        assert b'This field is required.' in res.data


class TestDisplayWeights2:

    # GETS
    def test_get_webpage_with_no_run_id(self, client):

        res = client.get('/manage_run/weights_2')
        assert res.status_code == 404

    def test_get_webpage_with_valid_data_selection_renders_portroute_column(self, client):

        res = client.get('/manage_run/weights_2/9e5c1872-3f8e-4ae5-85dc-c67a602d011e/SHIFT_DATA/Shift Data/0')
        assert b'Portroute' in res.data
        assert res.status_code == 200

    def test_get_webpage_with_valid_data_selection_renders_weekday_column(self, client):

        res = client.get('/manage_run/weights_2/9e5c1872-3f8e-4ae5-85dc-c67a602d011e/SHIFT_DATA/Shift Data/0')
        assert b'Weekday' in res.data
        assert res.status_code == 200

    def test_get_webpage_with_valid_data_selection_renders_arrivedepart_column(self, client):
        res = client.get('/manage_run/weights_2/9e5c1872-3f8e-4ae5-85dc-c67a602d011e/SHIFT_DATA/Shift Data/0')
        assert b'Arrivedepart' in res.data
        assert res.status_code == 200

    def test_get_webpage_with_valid_data_selection_renders_am_pm_night_column(self, client):
        res = client.get('/manage_run/weights_2/9e5c1872-3f8e-4ae5-85dc-c67a602d011e/SHIFT_DATA/Shift Data/0')
        assert b'Am Pm Night' in res.data
        assert res.status_code == 200

    def test_get_webpage_with_valid_data_selection_renders_total_column(self, client):
        res = client.get('/manage_run/weights_2/9e5c1872-3f8e-4ae5-85dc-c67a602d011e/SHIFT_DATA/Shift Data/0')
        assert b'Total' in res.data
        assert res.status_code == 200

    # Invalid data source
    def test_get_webpage_with_invalid_data_source_opens_page_with_table_title(self, client):
        res = client.get('/manage_run/weights_2/9e5c1872-3f8e-4ae5-85dc-c67a602d011e/SHIFT_DATA/Shift Data/10')
        assert b'Shift Data' in res.data
        assert res.status_code == 200

    def test_get_webpage_with_invalid_data_source_renders_no_records_error(self, client):
        res = client.get('/manage_run/weights_2/9e5c1872-3f8e-4ae5-85dc-c67a602d011e/SHIFT_DATA/Shift Data/10')
        assert b'No Records to show...' in res.data
        assert res.status_code == 200

    # No Records
    def test_get_webpage_with_valid_data_selection_but_no_records_in_opens_page_with_table_title(self, client):
        res = client.get('/manage_run/weights_2/9e5c1872-3f8e-4ae5-85dc-c67a6d011e/SHIFT_DATA/Shift Data/0')
        assert b'Shift Data' in res.data
        assert res.status_code == 200

    def test_get_webpage_with_valid_data_selection_but_no_records_in_table_renders_no_records_error(self, client):
        res = client.get('/manage_run/weights_2/9e5c1872-3f8e-4ae5-85dc-c67a6d011e/SHIFT_DATA/Shift Data/0')
        assert b'No Records to show...' in res.data
        assert res.status_code == 200

    # Invalid Table Name
    def test_get_webpage_using_incorrect_table_name_renders_no_records_error(self, client):
        res = client.get('/manage_run/weights_2/9e5c1872-3f8e-4ae5-85dc-c67a602d011e/FAKE_TABLE/Shift Data/0')
        assert b'No Records to show...' in res.data
        assert res.status_code == 200


    #POST

    # Export Button
    @pytest.mark.skip(reason="Functionality Not Implemented.")
    def test_pressing_export_button_triggers_redirect(self, client):
        pass

    @pytest.mark.skip(reason="Functionality Not Implemented.")
    def test_pressing_export_button_gets_correct_target_page(self, client):
        pass
