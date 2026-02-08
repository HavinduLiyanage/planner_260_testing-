import pytest
from logic.question_one.A import A

def test_a_uses_b(mocker):
    mock_b = mocker.Mock()  # Create a mock of B using pytest-mock
    mock_b.process.return_value = "mocked result"  # Define return value for the mocked method

    a = A(mock_b)  # Inject the mock into A
    result = a.run()  # Call the method that uses the mock

    assert result == "mocked result"  # Assert the result is what we defined in the mock
    mock_b.process.assert_called_once()  # Verify the mock method was called once

def test_a_uses_b_deny_access(mocker):
    pass # DELETE THIS
    #FILL MISSING CODE Create a mock of B using pytest-mock
    #FILL MISSING CODE Define return value for the mocked method deny access from Class B

    #FILL MISSING CODE Inject the mock into A
    #result = a.do_not_run(2)  # Call the method that uses the mock

    #assert result == "mocked result: error 2"  # Assert the result is what we defined in the mock
    #mock_b.deny_access.assert_called_once()  # Verify the mock method was called once