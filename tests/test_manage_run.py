from ips.forms import ManageRunForm
import pytest
import ips as web

app = web.app

@pytest.fixture()
def client():
    """The flask test client for our app.

    This lets us trigger http requests to end points without needing a server running.
    """

    app.testing = True
    app.config["WTF_CSRF_ENABLED"] = False
    client = app.test_client()


    return client


class TestManageRun:

    # GETS
    def test_get_webpage_with_no_run_id(self, client):

        res = client.get('/manage_run')
        assert res.status_code == 404

    def test_get_webpage_using_valid_run_id(self, client):


        res = client.get('/manage_run/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert res.status_code == 200
        assert b'9e5c1872-3f8e-4ae5-85dc-c67a602d011e' in res.data

    def test_get_webpage_using_invalid_run_id(self, client):

        res = client.get('/manage_run/9e5c1872-3f8e-4ae5-85dc-c67a602d0')
        assert res.status_code == 404
        assert b'9e5c1872-3f8e-4ae5-85dc-c67a602d011e' not in res.data

    def test_get_step_logs_renders_correctly(self, client):

        # get the web page
        res = client.get('/manage_run/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')

        assert b'Warning' in res.data

        assert b'Error' in res.data

        assert b'9e5c1872-3f8e-4ae5-85dc-c67a602d011e' in res.data


    # POSTS

    # Edit Data button
    def test_pressing_edit_data_button_triggers_redirect(self, client):

        with app.test_request_context():
            # Setup form submission information
            selection = ManageRunForm.edit_button
            data = {'edit_button': 'True'}
            # Post to weights with valid form data
            res = client.post('/manage_run/9e5c1872-3f8e-4ae5-85dc-c67a602d011e', data=data)

        # Ensure redirect target found
        assert res.status_code == 302
        # Ensure redirecting
        assert b'Redirecting' in res.data

    def test_pressing_edit_data_button_gets_correct_target_page(self, client):

        with app.test_request_context():
            # Setup form submission information
            selection = ManageRunForm.edit_button
            data = {'edit_button': 'True'}
            # Post to weights with valid form data
            res = client.post('/manage_run/9e5c1872-3f8e-4ae5-85dc-c67a602d011e', data=data)

        # Ensure target is new_run_1
        assert b'/new_run_1' in res.data

    def test_pressing_edit_data_button_triggers_no_validation_errors(self, client):

        with app.test_request_context():
            # Setup form submission information
            selection = ManageRunForm.edit_button
            data = {'edit_button': 'True'}
            # Post to weights with valid form data
            res = client.post('/manage_run/9e5c1872-3f8e-4ae5-85dc-c67a602d011e', data=data)

        # Ensure validation passed
        assert b'This field is required.' not in res.data

    # Display Weights button
    def test_pressing_display_weights_button_triggers_redirect(self, client):

        with app.test_request_context():
            # Setup form submission information
            selection = ManageRunForm.display_button
            data = {'display_button': 'True'}
            # Post to weights with valid form data
            res = client.post('/manage_run/9e5c1872-3f8e-4ae5-85dc-c67a602d011e', data=data)

        # Ensure redirect target found
        assert res.status_code == 302
        # Ensure redirecting
        assert b'Redirecting' in res.data

    def test_pressing_display_weights_button_gets_correct_target_page(self, client):

        with app.test_request_context():
            # Setup form submission information
            selection = ManageRunForm.display_button
            data = {'display_button': 'True'}
            # Post to weights with valid form data
            res = client.post('/manage_run/9e5c1872-3f8e-4ae5-85dc-c67a602d011e', data=data)

        # Ensure target is weights_2
        assert b'/weights' in res.data

    def test_pressing_display_weights_button_triggers_no_validation_errors(self, client):

        with app.test_request_context():
            # Setup form submission information
            selection = ManageRunForm.display_button
            data = {'display_button': 'True'}
            # Post to weights with valid form data
            res = client.post('/manage_run/9e5c1872-3f8e-4ae5-85dc-c67a602d011e', data=data)

        # Ensure validation passed
        assert b'This field is required.' not in res.data

    # Manage Run button
    def test_pressing_manage_run_button_triggers_redirect(self, client):

        with app.test_request_context():
            # Setup form submission information
            selection = ManageRunForm.edit_button
            data = {'manage_run_button': 'True'}
            # Post to weights with valid form data
            res = client.post('/manage_run/9e5c1872-3f8e-4ae5-85dc-c67a602d011e', data=data)

        # Ensure redirect target found
        assert res.status_code == 302
        # Ensure redirecting
        assert b'Redirecting' in res.data

    def test_pressing_manage_run_button_gets_correct_target_page(self, client):
        with app.test_request_context():
            # Setup form submission information
            selection = ManageRunForm.edit_button
            data = {'manage_run_button': 'True'}
            # Post to weights with valid form data
            res = client.post('/manage_run/9e5c1872-3f8e-4ae5-85dc-c67a602d011e', data=data)

        # Ensure target is manage_run/<run_id>
        assert b'/manage_run/9e5c1872-3f8e-4ae5-85dc-c67a602d011e' in res.data

    def test_pressing_manage_run_button_triggers_no_validation_errors(self, client):
        with app.test_request_context():
            # Setup form submission information
            selection = ManageRunForm.edit_button
            data = {'manage_run_button': 'True'}
            # Post to weights with valid form data
            res = client.post('/manage_run/9e5c1872-3f8e-4ae5-85dc-c67a602d011e', data=data)

        # Ensure validation passed
        assert b'This field is required.' not in res.data

    # Export Tab
    def test_pressing_export_tab_triggers_redirect(self, client):

        with app.test_request_context():
            # Setup form submission information
            selection = ManageRunForm.edit_button
            data = {'export_button': 'True'}
            # Post to weights with valid form data
            res = client.post('/manage_run/9e5c1872-3f8e-4ae5-85dc-c67a602d011e', data=data)

        # Ensure redirect target found
        assert res.status_code == 302
        # Ensure redirecting
        assert b'Redirecting' in res.data

    def test_pressing_export_tab_gets_correct_target_page(self, client):

        with app.test_request_context():
            # Setup form submission information
            selection = ManageRunForm.edit_button
            data = {'export_button': 'True'}
            # Post to weights with valid form data
            res = client.post('/manage_run/9e5c1872-3f8e-4ae5-85dc-c67a602d011e', data=data)

        # Ensure target is export_data/<run_id>
        assert b'/reference_export/9e5c1872-3f8e-4ae5-85dc-c67a602d011e' in res.data

    def test_pressing_export_tab_triggers_no_validation_errors(self, client):

        with app.test_request_context():
            # Setup form submission information
            selection = ManageRunForm.edit_button
            data = {'export_button': 'True'}
            # Post to weights with valid form data
            res = client.post('/manage_run/9e5c1872-3f8e-4ae5-85dc-c67a602d011e', data=data)

        # Ensure validation passed
        assert b'This field is required.' not in res.data

    # Run button
    @pytest.mark.skip(reason="Functionality Not Implemented.")
    def test_pressing_run_button(self, client):
        with app.test_request_context():
            # Setup form submission information
            selection = ManageRunForm.run_button
            data = {'run_button': 'True'}
            # Post to weights with valid form data
            res = client.post('/manage_run/9e5c1872-3f8e-4ae5-85dc-c67a602d011e', data=data)

        # Functionality has yet be be set up
        assert False