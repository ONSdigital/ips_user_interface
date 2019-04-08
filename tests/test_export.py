import pytest

import ips as web
from ips.forms import ExportSelectionForm

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


class TestExports:

    # GET tests

    def test_get_manage_run_webpage_no_run_id_returns_fail_status(self, client):
        res = client.get('/manage_run/export_data/')
        assert res.status_code == 404

    def test_get_manage_run_webpage_using_invalid_run_id(self, client):
        res = client.get('/manage_run/export_data/not-a-valid-run')
        assert res.status_code == 404
        assert b'9e5c1872-3f8e-4ae5-85dc-c67a602d011e' not in res.data

    def test_get_export_table_webpage_valid_run(self, client):
        res = client.get('/reference_export/9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
        assert res.status_code == 200
        assert b'9e5c1872-3f8e-4ae5-85dc-c67a602d011e' in res.data

    def test_get_export_table_webpage_invalid_run(self, client):
        res = client.get('/reference_export/not-a-valid-run')
        assert res.status_code == 404
        assert b'9e5c1872-3f8e-4ae5-85dc-c67a602d011e' not in res.data

    def test_export_data_posts_gets_deletes_data(self, client):
        # Test data to delete, post and get
        with app.test_request_context():
            # Setup form submission information
            data = {'data_selection': 'PS_IMBALANCE', 'filename': 'this-is-a-testing-file'}
            # Post with valid form data
            post_response = client.post('/export_data/9e5c1872-3f8e-4ae5-85dc-c67a602d011e', data=data)

            # Post should be 302
            assert post_response.status_code == 302

    # POST tests

    # Edit Data button
    def test_pressing_export_button_triggers_redirect_with_no_validation_errors(self, client):
        with app.test_request_context():
            # Setup form submission information
            selection = ExportSelectionForm.display_data
            data = {'data_selection': 'PS_IMBALANCE', 'filename': 'test'}
            # Post to weights with valid form data
            res = client.post('/export_data/9e5c1872-3f8e-4ae5-85dc-c67a602d011e', data=data)

        # Ensure redirect target found
        assert res.status_code == 302
        # Ensure redirecting
        assert b'Redirecting' in res.data
        # Ensure validation passed
        assert b'This field is required.' not in res.data
