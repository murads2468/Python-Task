
def evaluate_expression(expression):

    if not isinstance(expression, str):
        raise TypeError("Expression must be a string")

    if not expression.strip():
        raise ValueError("Expression cannot be empty")

    values = []
    operators = []

    def calculate():

        operator = operators.pop()

        if operator == "u-":
            if not values:
                raise ValueError("Invalid expression")
            values.append(-values.pop())
            return

        if len(values) < 2:
            raise ValueError("Invalid expression")

        b = values.pop()
        a = values.pop()

        if operator == "+":
            values.append(a + b)

        elif operator == "-":
            values.append(a - b)

        elif operator == "*":
            values.append(a * b)

        elif operator == "/":
            if b == 0:
                raise ZeroDivisionError("Division by zero")
            values.append(a / b)

    def precedence(operator):
        if operator == "u-":
            return 3
        if operator in ("*", "/"):
            return 2
        return 1

    index = 0
    expecting_number = True

    try:

        while index < len(expression):

            char = expression[index]

            if char.isspace():
                index += 1
                continue

            # Read integer numbers
            if char.isdigit():

                if not expecting_number:
                    raise ValueError("Missing operator")

                number = ""

                while index < len(expression) and expression[index].isdigit():
                    number += expression[index]
                    index += 1

                values.append(int(number))
                expecting_number = False
                continue

            # Opening parenthesis
            elif char == "(":

                if not expecting_number:
                    raise ValueError("Missing operator")

                operators.append(char)
                index += 1
                continue

            # Closing parenthesis
            elif char == ")":

                if expecting_number:
                    raise ValueError("Invalid expression")

                while operators and operators[-1] != "(":
                    calculate()

                if not operators:
                    raise ValueError("Unmatched parenthesis")

                operators.pop()
                index += 1

                # Apply unary minus before parentheses
                while operators and operators[-1] == "u-":
                    calculate()

                expecting_number = False
                continue

            # Operators
            elif char in "+-*/":

                if expecting_number:

                    if char == "-":
                        operators.append("u-")
                        index += 1
                        continue

                    raise ValueError("Invalid operator")

                while (
                    operators
                    and operators[-1] != "("
                    and precedence(operators[-1]) >= precedence(char)
                ):
                    calculate()

                operators.append(char)
                expecting_number = True
                index += 1
                continue

            else:
                raise ValueError("Invalid character found")

        if expecting_number:
            raise ValueError("Incomplete expression")

        while operators:
            if operators[-1] == "(":
                raise ValueError("Unmatched parenthesis")

            calculate()

        if len(values) != 1:
            raise ValueError("Invalid expression")

        return float(values[0])

    except IndexError:
        raise ValueError("Invalid expression")


# Test expression
expression = "-(3 + 2) * 4 + 18 / 3"

print(evaluate_expression(expression))
