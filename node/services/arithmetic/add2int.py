def add_two_numbers(num1: int, num2: int):
    if num1 is None or num2 is None:
        raise ValueError("Both numbers must be provided.")
    return num1 + num2