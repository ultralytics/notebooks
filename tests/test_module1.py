# Ultralytics YOLO 🚀, AGPL-3.0 License https://ultralytics.com/license

from module1 import add_numbers


def test_add_numbers():
    """
    Test the add_numbers function from module1 by verifying the correctness of summation operation between pairs of
    integers.

    Tests:
      - Ensures that the sum of 2 and 3 equals 5.
      - Validates that the sum of -1 and 1 equals 0.

    Returns:
      (None): This function performs assertions to validate the behavior of add_numbers. It does not return a value.

    Raises:
      AssertionError: If any of the assertions fail, this error is raised indicating a test case failure.
    """
    assert add_numbers(2, 3) == 5
    assert add_numbers(-1, 1) == 0
    assert add_numbers(-1, -1) == -2
