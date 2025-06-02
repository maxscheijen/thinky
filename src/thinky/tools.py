from agents import function_tool


@function_tool
def add_numbers(a: int, b: int) -> int:
    """Add two numbers.

    Args:
        a (int): The first number.
        b (int): The second number.
    """
    return a + b
