from ips.forms import SearchActivityForm
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


class TestDashboard:

    # GETS
    def test_get_webpage_returns_ok_status(self, client):
        res = client.get('/dashboard/')
        assert res.status_code == 200

    def test_get_webpage_returns_ok_status(self, client):
        res = client.get('/dashboard/')
        assert b'Run Id' in res.data

    def test_get_webpage_contains_run_name_column(self, client):
        res = client.get('/dashboard/')
        assert b'Run Name' in res.data

    def test_get_webpage_contains_run_description_column(self, client):
        res = client.get('/dashboard/')
        assert b'Run Description' in res.data

    def test_get_webpage_contains_start_date_column(self, client):
        res = client.get('/dashboard/')
        assert b'Start Date' in res.data

    def test_get_webpage_contains_end_date_column(self, client):
        res = client.get('/dashboard/')
        assert b'End Date' in res.data

    def test_get_webpage_contains_type_column(self, client):
        res = client.get('/dashboard/')
        assert b'Type' in res.data

    def test_get_webpage_contains_status_column(self, client):
        res = client.get('/dashboard/')
        assert b'Status' in res.data

    # POSTS
    def test_pressing_search_button_returns_same_webpage(self, client):
        with app.test_request_context():
            # Setup form submission information
            form = SearchActivityForm(search_button=True)
            # Post to dashboard
            res = client.post('/dashboard/', data=form.data)

        # Ensure ok status code
        assert res.status_code == 200
        # Ensure page search activity exists
        assert b'Search activity' in res.data

    def test_pressing_search_button_returns_records_to_display(self, client):
        with app.test_request_context():
            # Setup form submission information
            form = SearchActivityForm(search_button=True)
            # Post to dashboard
            res = client.post('/dashboard/', data=form.data)

        # Ensure ok status code
        assert res.status_code == 200
        # Enusre records are showing
        assert b'9e5c1872-3f8e-4ae5-85dc-c67a602d011e' in res.data

    def test_pressing_search_button_with_live_in_field_returns_records_containing_live(self, client):
        with app.test_request_context():
            # Setup form submission information
            form = SearchActivityForm(search_button=True, search_activity='190218')
            # Post to weights with valid form data
            res = client.post('/dashboard/', data=form.data)

        # Ensure redirect target found
        assert res.status_code == 200
        # Ensure redirecting
        assert b'a97e0960-6a49-402b-a784-ec5c3c2d74ef' in res.data
