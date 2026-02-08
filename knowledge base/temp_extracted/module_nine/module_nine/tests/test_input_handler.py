import pytest
from logic.input_handler import collect_user_details, menu_system


# ------------------------
# Test 1: Monkeypatching input for sequential input collection
# ------------------------

def test_collect_user_details(monkeypatch):
    # Define the sequence of inputs to simulate user typing
    inputs = iter(["Alice", "30", "alice@example.com", "Wonderland"])

    # Replace the built-in input function with a lambda that returns the next item from the inputs iterator
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    # Call the function under test, which will use our monkeypatched input
    result = collect_user_details()

    # Define the expected output string based on the mocked input
    expected = "User: Alice, Age: 30, Email: alice@example.com, Country: Wonderland"

    # Verify the function output matches the expected result
    assert result == expected


# ------------------------
# Test 2: Monkeypatching input and capturing output (capsys)
# ------------------------

# Parametrize test to run multiple scenarios with different user inputs and expected outputs
@pytest.mark.parametrize("input_val,expected_output", [
    ("1", "Hello, User!"),  # Test case for option 1
    ("2", "Goodbye, User!"),  # Test case for option 2
    ("3", "Exiting..."),  # Test case for option 3
    ("invalid", "Invalid option selected."),  # Test case for invalid input
])
def test_menu_system(monkeypatch, capsys, input_val, expected_output):
    # Monkeypatch input() to return the current test's input_val
    monkeypatch.setattr("builtins.input", lambda _: input_val)

    # Call the function which prints to stdout based on input
    menu_system()

    # Capture the printed output from stdout using capsys
    captured = capsys.readouterr()

    # Check if the expected output is found in the captured output
    assert expected_output in captured.out