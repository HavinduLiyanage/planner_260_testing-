import pytest
from logic.question_three.ReportGenerator import ReportGenerator

@pytest.fixture
def mock_fetcher(mocker):
    mock = mocker.Mock()  # Mock the DataFetcher
    mock.fetch.return_value = {"value": 123}  # Define return value
    return mock

@pytest.fixture
def mock_formatter(mocker):
    mock = mocker.Mock()  # Mock the Formatter
    mock.format.return_value = "Formatted: {'value': 123}"  # Define return value
    return mock

def test_report_generator(mock_fetcher, mock_formatter):
    generator = ReportGenerator(mock_fetcher, mock_formatter)  # Inject mocks
    result = generator.generate()  # Run the method under test

    assert result == "Formatted: {'value': 123}"  # Validate output
    mock_fetcher.fetch.assert_called_once()  # Ensure fetch was called once
    mock_formatter.format.assert_called_once_with({"value": 123})  # Ensure format was called with expected input

def test_report_generator_formatter_integration(mock_fetcher):
    pass
