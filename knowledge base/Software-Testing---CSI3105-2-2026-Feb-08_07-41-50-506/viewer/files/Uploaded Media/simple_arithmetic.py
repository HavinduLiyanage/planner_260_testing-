# simple_arithmetic.py

class SimpleArithmetic:
    def add_two_no(self, num1, num2):
        return num1 + num2

    def sub_two_no(self, num1, num2):
        return num1 - num2

    def mul_two_no(self, num1, num2):
        return num1 * num2

    def div_int_two_no(self, num1, num2):
        if num2 == 0:
            raise ValueError("Cannot divide by 0!")
        return num1 // num2  # Integer division

    def div_real_two_no(self, num1, num2):
        if num2 == 0:
            raise ValueError("Cannot divide by 0!")
        return num1 / num2  # Floating point division
