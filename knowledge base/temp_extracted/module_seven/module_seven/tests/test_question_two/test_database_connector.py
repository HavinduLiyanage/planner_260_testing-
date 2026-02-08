import pytest
from logic.question_two.DatabaseConnector import DatabaseConnector
from logic.question_two.DummyDB import DummyDB


@pytest.fixture
def monkeypatched_input(mocker):
    mocker.patch("builtins.input", side_effect=["localhost", "localhost"])  # Monkeypatch input() to simulate user entry

def test_connector_with_mocked_db(monkeypatched_input, mocker):
    host, port = DatabaseConnector.from_user_input()  # Simulate user input to get host and port values

    mock_db = mocker.Mock(spec=DummyDB)  # Create a mock of DummyDB that adheres to its interface
    mock_db.connect.return_value = f"Connected to {host}:{port}"  # Set expected return value for connect()

    connector = DatabaseConnector(mock_db)  # Inject the mock DB into our connector
    result = connector.connect()  # Call the connect method which should delegate to our mock

    assert result == "Connected to localhost:localhost"  # Assert the return value is what we expect
    mock_db.connect.assert_called_once()  # Verify that connect() was called exactly once on the mock
