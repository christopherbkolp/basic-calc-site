from django.test import TestCase
from calc.calculator import Calculate

class BasicMathTestCase(TestCase):
    def test_exponent(self):
        user = Calculate()
        result = user.perform_exp(8, 3)
        self.assertEqual(result, 512)

    def test_multiplication(self):
        user = Calculate()
        result = user.perform_mul(8, 8)
        self.assertEqual(result, 64)

    def test_division(self):
        user = Calculate()
        result = user.perform_div(8, 4)
        self.assertEqual(result, 2)

    def test_addition(self):
        user = Calculate()
        result = user.perform_add(8, 9)
        self.assertEqual(result, 17)

    def test_subtraction(self):
        user = Calculate()
        result = user.perform_sub(8, 3)
        self.assertEqual(result, 5)

class ErrorTestCase(TestCase):
    def test_exit_1(self):
        user = Calculate()
        user.get_equation('(8*(8*8)))')
        try:
            user.math_check()
            raise ValueError('System Exit 1 is not working as intended.')
        except SystemExit:
            self.assertEqual(user.error_msg, 'Error: Invalid number of Parentheses')

    def test_exit_2(self):
        user = Calculate()
        expression = ['8','*','8','%']
        try:
            user.run_expression(expression)
            raise ValueError('System Exit 2 is not working as intended.')
        except SystemExit:
            self.assertEqual(user.error_msg, 'Error: Invalid Expression')

    def test_exit_3(self):
        user = Calculate()
        user.get_equation('5*f/26-8')
        try:
            user.math_check()
            raise ValueError('System Exit 3 is not working as intended.')
        except SystemExit:
            self.assertEqual(user.error_msg, "Error: This calculator does not support variables."
                f" Please remove: 'f'")

    def test_exit_4(self):
        user = Calculate()
        try:
            user.get_equation('8*')
            raise ValueError('System Exit 4 is not working as intended.')
        except SystemExit:
            self.assertEqual(user.error_msg, 'Error: Missing Value')

    def test_exit_5_version_1(self):
        user = Calculate()
        user.get_equation('8(8*8)')
        try:
            user.math_check()
            raise ValueError('System Exit 5 is not working as intended.')
        except SystemExit:
            self.assertEqual(user.error_msg, 'Error: This calculator does not support the Distributive Property currently.')

    def test_exit_5_version_2(self):
        user = Calculate()
        user.get_equation('(8(8*8))')
        try:
            user.math_check()
            raise ValueError('System Exit 5 is not working as intended.')
        except SystemExit:
            self.assertEqual(user.error_msg, 'Error: This calculator does not support the Distributive Property currently.')

    def test_exit_6(self):
        user = Calculate()
        try:
            user.get_equation('8//8')
            raise ValueError('System Exit 6 is not working as intended.')
        except SystemExit:
            self.assertEqual(user.error_msg, "Error: Invalid operator placement: '//'")

    def test_exit_7(self):
        user = Calculate()
        try:
            user.get_equation('8++8')
            raise ValueError('System Exit 7 is not working as intended.')
        except SystemExit:
            self.assertEqual(user.error_msg, "Error: Invalid operator placement: '++'")

    def test_exit_8(self):
        user = Calculate()
        try:
            user.get_equation('8--8')
            raise ValueError('System Exit 8 is not working as intended.')
        except SystemExit:
            self.assertEqual(user.error_msg, "Error: Invalid operator placement '--'")

class RunMathTestCase(TestCase):

    def test_exp_positive(self):
        user = Calculate()
        testmath = ['8', '**', '8']
        user.run_math('**', testmath)
        self.assertEqual(int(testmath[0]), 16777216)

    def test_mul_positive(self):
        user = Calculate()
        testmath = ['24', '*', '22']
        user.run_math('*', testmath)
        self.assertEqual(int(testmath[0]), 528)

    def test_div_positive(self):
        user = Calculate()
        testmath = ['12', '/', '4']
        user.run_math('/', testmath)
        self.assertEqual(int(testmath[0]), 3)

    def test_add_positive(self):
        user = Calculate()
        testmath = ['13', '+', '18']
        user.run_math('+', testmath)
        self.assertEqual(int(testmath[0]), 31)

    def test_sub_positive(self):
        user = Calculate()
        testmath = ['12', '-', '4']
        user.run_math('-', testmath)
        self.assertEqual(int(testmath[0]), 8)

    def test_exp_negative(self):
        user = Calculate()
        testmath = ['-8', '**', '3']
        user.run_math('**', testmath)
        self.assertEqual(int(testmath[0]), -512)

    def test_mul_negative(self):
        user = Calculate()
        testmath = ['24', '*', '-22']
        user.run_math('*', testmath)
        self.assertEqual(int(testmath[0]), -528)

    def test_div_negative(self):
        user = Calculate()
        testmath = ['12', '/', '-4']
        user.run_math('/', testmath)
        self.assertEqual(int(testmath[0]), -3)

    def test_add_negative(self):
        user = Calculate()
        testmath = ['-13', '+', '18']
        user.run_math('+', testmath)
        self.assertEqual(int(testmath[0]), 5)

    def test_sub_negative(self):
        user = Calculate()
        testmath = ['4', '-', '12']
        user.run_math('-', testmath)
        self.assertEqual(int(testmath[0]), -8)

    def test_exp_decimal_1(self):
        user = Calculate()
        testmath = ['0.5', '**', '3']
        user.run_math('**', testmath)
        self.assertEqual(float(testmath[0]), 0.125)

    def test_exp_decimal_2(self):
        user = Calculate()
        testmath = ['3', '**', '0.5']
        user.run_math('**', testmath)
        self.assertEqual(float(testmath[0]), 1.7320508075688772)

    def test_mul_decimal(self):
        user = Calculate()
        testmath = ['24', '*', '0.2']
        user.run_math('*', testmath)
        self.assertEqual(float(testmath[0]), 4.8)

    def test_div_decimal(self):
        user = Calculate()
        testmath = ['12', '/', '0.8']
        user.run_math('/', testmath)
        self.assertEqual(float(testmath[0]), 15)

    def test_add_decimal(self):
        user = Calculate()
        testmath = ['13', '+', '18.675']
        user.run_math('+', testmath)
        self.assertEqual(float(testmath[0]), 31.675)

    def test_sub_decimal(self):
        user = Calculate()
        testmath = ['12', '-', '4.5']
        user.run_math('-', testmath)
        self.assertEqual(float(testmath[0]), 7.5)

class RunExpressionTestCase(TestCase):

    def test_exp_expression(self):
        user = Calculate()
        testmath = '8**2**2'
        user.get_equation(testmath)
        user.run_expression(user.equation)
        self.assertEqual(user.result, 4096)
