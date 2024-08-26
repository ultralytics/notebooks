# Ultralytics YOLO 🚀, AGPL-3.0 License https://ultralytics.com/license


def add_numbers(a, b):
    """
    Adds two numbers and returns the sum.

    Args:
        a (float | int): The first number in the addition.
        b (float | int): The second number in the addition.

    Returns:
        (float | int): The sum of `a` and `b`.

    Notes:
        This function supports both integer and floating-point numbers. The returned value will match the type of the input
        values unless they're mixed, in which case a float is returned.

    Examples:
        ```python
        result = add_numbers(3, 5)
        assert result == 8

        result = add_numbers(3.5, 2)
        assert result == 5.5
        ```
    """
    return a + b
