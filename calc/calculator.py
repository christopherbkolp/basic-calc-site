from decimal import Decimal
import sys
import math
import copy
# Everything runs inside Calc, to use it set self
# and then run self.parentheses_check(). It will
# then ask for an equation and run it. If you want the
# answer printed, run self.print_result()

# WARNING: This calculator does not support variables.

class Calculate:
    def __init__(self):
        # Sets up the equation objects and
        # symbol dictionary.
        self.error_msg = 0
        self.equation = []
        self.result = ''
        self.symboldict = {
          "*": "mul",
          "/": "div",
          "+": "add",
          "-": "sub",
          "**": "exp",
        }

        # These need to be set once and never again.
        self.check1 = '('
        self.check2 = ')'

        # Setting up lists of every value with parentheses in it.
        # Adds 'end_list' to the lists to prevent index errors later.
        self.res = []
        self.res2 = []

    def get_equation(self, math):

        """
        Asks the user for a math equation to run

        Sets a list, this list holds the equation before being processed
        """

        # Local variables
        operators_list_split = []
        index_count = 0
        loop_number = 0

        # Checks for mathematical operators
        for char in math:
            if char in ('*', '/'):
                operators_list_split.append(char)
                loop_number = loop_number + 1
            elif char in ('+', '-'):
                operators_list_split.append(char)
                loop_number = loop_number + 1

        # Inserts '&' next to operators
        for value in operators_list_split:
            index = math.index(value, index_count)
            math = math[:index + 1] + '&' + math[index + 1:]
            math = math[:index] + '&' + math[index:]
            index_count = index + 2

        # Splits from '&' and then counts for whitespace.
        math = math.split('&')
        whitespace_count = math.count('')

        # Eliminates whitespace and fixes exponent signs.
        while whitespace_count > 0:
            index = math.index('')
            try:
                left_value = math[index - 1]
                right_value = math[index + 1]
            except IndexError:
                self.error_msg = "Error: Missing Value"
                sys.exit(4)

            if left_value == '*' and right_value == '*':
                math[index - 1 : index + 2] = [''.join(math[index - 1 : index + 2])]
                whitespace_count = whitespace_count - 1
            elif left_value == '/' and right_value == '/':
                self.error_msg = "Error: Invalid operator placement: '//'"
                sys.exit(6)
            elif left_value == '+' and right_value == '+':
                self.error_msg = "Error: Invalid operator placement: '++'"
                sys.exit(7)
            elif left_value == '-' and right_value == '-':
                self.error_msg = "Error: Invalid operator placement '--'"
                sys.exit(8)

        # Checks if the expression is only 1 value
        if len(math) == 1:
            math[0] = math[0].replace('(', '')
            math[0] = math[0].replace(')', '')

        # Returns the processed input
        self.equation = math

    def run_parentheses(self):

        """
        This function finds the parentheses that have been found and runs the
        math inside them. It also replaces the parentheses with the result of
        the math done inside them.
        """

        # Setting up local variables
        res_increment = 0
        index_increment = 0
        calc_found = False
        open_para_pos = None
        close_para_pos = None

        # This while loop checks for the position of open parentheses in
        # self.equation. When it finds the corresponding close parentheses
        # it then logs the index of the open and close parentheses it finds.
        # It also sets up the working_list which is what the math is actually run in.
        while not calc_found:
            for element in self.equation:
                if self.res[res_increment] == element:
                    res_increment = res_increment + 1
                    open_para_pos = self.equation.index(element, index_increment)
                    index_increment = open_para_pos + 1

                if self.res2[0] == element:
                    close_para_pos = self.equation.index(element)
                    del self.res[res_increment - 1]
                    del self.res2[0]
                    working_list = self.equation[open_para_pos: close_para_pos + 1]
                    calc_found = True
                    break

        # This checks for numbers in front of parentheses. Ex: 5(8 * 2)
        try:
            index_increment = 1
            for character in working_list[0]:
                if character == '(':
                    if working_list[0][working_list[0].index('(', index_increment) - 1].isnumeric():
                        self.error_msg = "Error: This calculator does not support the Distributive Property currently."
                        sys.exit(5)
                    else:
                        index_increment = character.index('(', index_increment) + 1
        except ValueError:
            pass

        # Deletes the parentheses in the working_list while leaving the numbers.
        # Then runs the math in working_list in the order of PEMDAS.
        working_list[0] = working_list[0].replace('(', '')
        working_list[-1] = working_list[-1].replace(')', '')
        self.run_expression(working_list)

        # This finds how many open and close parentheses were next to the numbers
        # found in self.equation.
        open_para_pos_count = self.equation[open_para_pos].count('(') - 1
        close_para_pos_count = self.equation[close_para_pos].count(')') - 1

        # Replaces the original segment of parentheses with the result of
        # running math on them. Ex: [(5 * 5)] --> [25]
        del self.equation[open_para_pos: close_para_pos + 1]
        self.equation.insert(open_para_pos, working_list[0])
        self.equation[open_para_pos] = str(self.equation[open_para_pos])

        # This If Else statement handles if there are more than one parentheses
        # next to the original numbers. This adds back parentheses that are still
        # required to run the equation the correct way.
        # Ex: [((5 * 5) - 3)] --> [(25 - 3)]
        if open_para_pos_count > 0 and close_para_pos_count > 0:
            open_count = '(' * open_para_pos_count
            self.equation[open_para_pos] = open_count + self.equation[open_para_pos]
            self.res.insert(res_increment - 1, self.equation[open_para_pos])

            close_count = ')' * close_para_pos_count
            self.equation[open_para_pos] = self.equation[open_para_pos] + close_count
            self.res2.insert(0, self.equation[open_para_pos])

        elif open_para_pos_count > 0:
            open_count = '(' * open_para_pos_count
            self.equation[open_para_pos] = open_count + self.equation[open_para_pos]
            self.res.insert(res_increment - 1, self.equation[open_para_pos])

        elif close_para_pos_count > 0:
            close_count = ')' * close_para_pos_count
            self.equation[open_para_pos] = self.equation[open_para_pos] + close_count
            self.res2.insert(0, self.equation[open_para_pos])

    def math_check(self):

        """
        This function checks for parentheses and then runs them if they were found
        in the list. If there are none it checks for math without parentheses.
        Finally, if there is no math anywhere it finishes as there is no math to run.
        """
        open_para_increment = 0
        close_para_increment = 0
        para_count = 0

        # Finding vaules with parentheses in them
        for value in self.equation:
            for char in value:
                if '(' == char:
                    self.res.append(value)
                    break
                if ')' == char:
                    self.res2.append(value)
                    break

        self.res.append('end_list')
        self.res2.append('end_list')


        # These for loops just check for letters/variables in the expression.
        # If there are none this doesn't affect anything.
        for element in self.equation:
            for letter in element:
                try:
                    alphabet_check = letter.isalpha()
                    if alphabet_check:
                        self.error_msg = ("Error: This calculator does not support variables."
                            f" Please remove: '{letter}'")
                        sys.exit(3)

                except (ValueError, AttributeError, TypeError):
                    alphabet_check = False

        # This For loop counts how many parentheses are inside self.equation.
        # This is used later for error checks, and looping for math inside all
        # the parentheses.
        for element in self.equation:
            element_index = self.equation.index(element)
            if self.res[open_para_increment] == element:
                para_count = para_count + self.equation[element_index].count('(')
                open_para_increment = open_para_increment + 1

            if self.res2[close_para_increment] == element:
                para_count = para_count + self.equation[element_index].count(')')
                close_para_increment = close_para_increment + 1

        # This If statement first checks if there are any parentheses.
        # Then if the nuber of open and close parentheses are equal in number.
        # And if none of those conditions are true, it exits with an error code.
        if para_count == 0 and para_count == 0:
            self.run_expression(self.equation)

        elif para_count % 2 == 0:
            # This while loop just runs until there are no more parentheses.
            while 0 < para_count:
                self.run_parentheses()
                para_count = para_count - 2

            # This is a check for anymore math to run after there are no more
            # parentheses.
            if len(self.equation) > 1:
                self.run_expression(self.equation)

        else:
            self.error_msg = 'Error: Invalid number of Parentheses'
            sys.exit(1)

    def run_math(self, operation, expression):

        """
        This is the function that directly runs math equations.

        :param operation: str, mathematical operator used in expression
        :param expression: list, expression is the math that is run in this function
        :returns: int, count of how many operators left in the expression
        """

        # This is getting the 3 letter word attributed to the math operation.
        symbol = self.symboldict[operation]
        operator_count = expression.count(operation)

        # This If statement actually runs the math expression given.
        # It first looks for an operator in the order of PEMDAS.
        # When one is found it then looks at the numbers to the left
        # and right of the operator. It then looks for the expression tied
        # to that particular operator. It then runs the two numbers through
        # that expression. Finally it replaces the numbers and operator with
        # the result it found.
        if operator_count > 0:
            operator_index = expression.index(operation)
            value1 = Decimal(expression[operator_index - 1])
            value2 = Decimal(expression[operator_index + 1])
            operator_expression = getattr(self, 'perform_' + symbol)
            result = operator_expression(value1, value2)
            del expression[operator_index - 1:operator_index + 2]
            expression.insert(operator_index - 1, result)
            operator_count = operator_count - 1
        return operator_count

    # This function block holds all the operator expressions.
    def perform_exp(self, value1, value2):
        return value1 ** value2
    def perform_mul(self, value1, value2):
        return value1 * value2
    def perform_div(self, value1, value2):
        return value1 / value2
    def perform_add(self, value1, value2):
        return value1 + value2
    def perform_sub(self, value1, value2):
        return value1 - value2

    def run_expression(self, expression):
        """
        # This fuction runs through the expression given with PEMDAS.

        :param expression: list, expression is the math that is run in this function
        """

        # Setting local variables and counting how many of each
        # operator are in the expression given.
        exp = expression.count('**')
        mul = expression.count('*')
        div = expression.count('/')
        add = expression.count('+')
        sub = expression.count('-')
        # import pdb; pdb.set_trace()


        # # TODO: Somethings wrong with this, unsure what however.
        # This just quickly does any exponents first
        while exp > 0:
            for element in expression:
                if '**' == element:
                    exp = self.run_math('**', expression)

        # This while loop is to help the function frun PEMDAS.
        # PEMDAS runs multiply and divide at the same time,
        # solving each as it goes. Then restarting at the beginning.
        # This while loop does that for multiply and divide.
        while mul > 0 or div > 0:
            for element in expression:
                if '*' == element:
                    mul = self.run_math('*', expression)
                elif '/' == element:
                    div = self.run_math('/', expression)

        # This while loop does the same thing as the other one,
        # just with addition and subtraction.
        while add > 0 or sub > 0:
            for element in expression:
                if '+' == element:
                    add = self.run_math('+', expression)
                elif '-' == element:
                    sub = self.run_math('-', expression)

        # This makes sure that only one value is left after running the expression.
        # It only triggers if there is an operator or number missing.
        if len(expression) == 1:
            pass
        else:
            self.error_msg = "Error: Invalid Expression"
            sys.exit(2)

        # This is simply setting the result up for printing, or to input
        # somewhere else.
        self.result = float(expression[0])

    def return_result(self):

        """
        This function returns the result
        """

        # This If statement just gets rid of a decimal of .0
        # If the decimal at the end is .01 it will keep it.
        try:
            if self.result.is_integer():
                self.result = int(self.result)
            else:
                pass

            decimal_present = False
            result_value = math.floor(self.result)
            self.result = str(self.result)
            if result_value > 3:
                index = -3

                result_value = str(result_value)
                result_len = len(result_value)

                if self.result.find('.') > 0:
                    print(self.result.find('.'))
                    decimal_present = True
                    decimal_index = self.result.find('.')
                    decimal_values = copy.deepcopy(self.result[decimal_index:])
                    self.result = self.result[:decimal_index]

                if result_len % 3 == 0:
                    result_len = result_len / 3
                    result_len = result_len - 1
                    for count in range(int(result_len)):
                        self.result = self.result[:index] + ',' + self.result[index:]
                        index = index - 4
                else:
                    result_len = result_len / 3
                    result_len = math.floor(result_len)

                    for count in range(int(result_len)):
                        self.result = self.result[:index] + ',' + self.result[index:]
                        index = index - 4

                if decimal_present == True:
                    self.result = self.result + decimal_values

            return self.result
        except OverflowError:
            if self.result == float('inf'):
                self.result = '∞'
                return self.result
            else:
                self.error_msg = 'Unknown Error: Please contact Docker maintainer.'
                sys.exit(9)
