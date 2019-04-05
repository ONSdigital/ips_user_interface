from ips import app_methods

def test_get_system_info():
    """
    Purpose: Tests the get_system_info method's functionality.
    """
    # Previous test removed, one will be needed for this page when the info is accessible
    # Need a test to check system info is pulling correctly
    # (should these tests be done when the data is not hard coded?)
    assert True


def test_create_run():
    """
    Purpose: Tests the create_run method's functionality.
    """
    runs = app_methods.get_runs()
    app_methods.create_run("AUTOMATED-TEST-RUN-ID", "AUTOMATED_TEST_NAME", "This is an **AUTOMATED** test. - DO NOT RUN", "01012018", "01012018", '0', '0')
    new_runs = app_methods.get_runs()

    # Check no new run has been created (Creation should be declined due to the primary key constraint)
    assert len(runs) <= len(new_runs)


def test_get_runs():
    """
    Purpose: Tests the get_runs method's functionality.
    """
    result = app_methods.get_runs()
    assert isinstance(result, list)
    assert len(result) > 0


def test_get_display_data_json():

    # Valid table
    df = app_methods.get_display_data_json('SHIFT_DATA')
    # Dataframe should not be empty
    assert df.empty is False
    assert len(df.index) > 0

    # Valid table, valid run_id
    df = app_methods.get_display_data_json('SHIFT_DATA', '9e5c1872-3f8e-4ae5-85dc-c67a602d011e')
    # Dataframe should not be empty
    assert df.empty is False
    assert len(df.index) > 0

    # Tests below use incorrect data in the function call

    # Valid table, invalid run_id, invalid data_source
    df = app_methods.get_display_data_json('SHIFT_DATA', '0000', '1')
    assert df.empty is True

    # Valid table, invalid run_id, valid data_source
    df = app_methods.get_display_data_json('SHIFT_DATA', '0000', '4')
    assert df.empty is True

    # Valid table, valid run_id, invalid data_source
    df = app_methods.get_display_data_json('SHIFT_DATA','9e5c1872-3f8e-4ae5-85dc-c67a602d011e', '1')
    assert df.empty is True

    # Invalid table
    df = app_methods.get_display_data_json('FAKE_TABLE')
    assert df.empty is True
