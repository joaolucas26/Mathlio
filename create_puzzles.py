import random


MAX_OPERATOR = 1
MAX_MULTIPLIER = 5
MAX_MULTIPLICANT = 9
MAX_NUMBER = 9
MIN_NUMBER = 1
MAX_MULTIPLICATION = 1
MAX_DIVISION = 1
EQUATION_PER_DAY = 3
MIN_RESULT = 1
MAX_RESULT = 99


OPERATORS = {'MULTIPLICATION': '*', 'DIVISION': '/',
             'ADDITION': '+', 'SUBTRACTION': '-'}


def main():
    daily_equations = []
    daily_numbers = []

    while (len(daily_equations) < EQUATION_PER_DAY):
        operators_selected = get_operators()
        
        numbers_selected = get_numbers(operators_selected)
        expression = get_expression(operators_selected, numbers_selected)
        result = solve_expression(expression)
       
        if (result < MIN_RESULT or result > MAX_RESULT and result == int(result)):
            continue

        equation = get_equation(expression, result)
        daily_equations.append(equation)
        puzzle_numbers = get_puzzle_numbers(numbers_selected + [result])
        daily_numbers = puzzle_numbers + daily_numbers

    returnado = {'daily_equations': daily_equations, 'puzzle': daily_numbers}
    #print('daily_equations', daily_equations)
    print('daily_numbers', daily_numbers)
    print('len', len(daily_numbers))
    return returnado


def get_operators():
    operators_selected = []
    operators_quantity = random.randint(1, MAX_OPERATOR)
    while (len(operators_selected) < operators_quantity):
        count_multiplication = operators_selected.count(
            OPERATORS['MULTIPLICATION'])
        count_division = operators_selected.count(OPERATORS['DIVISION'])

        valid_operators = []

        for value in OPERATORS.values():
            if value == OPERATORS['MULTIPLICATION'] and count_multiplication >= MAX_MULTIPLICATION:
                continue
            elif value == OPERATORS['DIVISION'] and count_division >= MAX_DIVISION:
                continue
            valid_operators.append(value)

        operator = random.choice(valid_operators)
        operators_selected.append(operator)

    return operators_selected


def get_numbers(operators_selected):
    numbers_quantity = len(operators_selected) + 1
    numbers_selected = []


    while(len(numbers_selected) < numbers_quantity):
        max_number = MAX_NUMBER
        index = len(numbers_selected)-1
        if index < numbers_quantity -2:
            next_operator = operators_selected[index+1]
            if next_operator == OPERATORS['DIVISION']:
                multiplicant = random.randint(MIN_NUMBER, MAX_MULTIPLICANT)
                multiplier = random.randint(MIN_NUMBER, MAX_MULTIPLIER)
                quocient = multiplicant * multiplier
                divident = quocient 
                divisor = multiplicant
                numbers_selected.append(divident)
                numbers_selected.append(divisor)
                continue
            
            elif next_operator == OPERATORS['MULTIPLICATION']:
                max_number = MAX_MULTIPLICANT
                

        if (index > 0):
            prev_operator = operators_selected[index]
            if prev_operator ==  OPERATORS['MULTIPLICATION']:
                max_number = MAX_MULTIPLIER
        
        number = random.randint(MIN_NUMBER, max_number)
        numbers_selected.append(number)
    
    return numbers_selected


def get_expression(operators_selected, numbers_selected):
    expression = []
    for i in range(len(numbers_selected)):
        expression.append(numbers_selected[i])
        if i < len(operators_selected):
            expression.append(operators_selected[i])

    return expression


def solve_expression(expression):
    '''determina quais as prioridades'''
    first_priority_operations = solve_operations(
        expression, [OPERATORS['MULTIPLICATION'], OPERATORS['DIVISION']])
    second_priority_operations = solve_operations(
        first_priority_operations, [OPERATORS['ADDITION'], OPERATORS['SUBTRACTION']])

    float_result = float(second_priority_operations[0])

    if float_result.is_integer():
        return int(float_result)
    else:
        return MAX_RESULT +1 


def calculate_operations(value1, value2, operator):

    if operator == OPERATORS['MULTIPLICATION']:
        return value1*value2
    elif operator == OPERATORS['DIVISION']:
        return value1/value2
    elif operator == OPERATORS['ADDITION']:
        return value1+value2
    elif operator == OPERATORS['SUBTRACTION']:
        return value1-value2


def solve_operations(expression, operators):
    for i in range(1, len(expression) - 1):
        char = expression[i]
        if char in operators:
            prev_char = expression[i-1]
            next_char = expression[i+1]
            result = calculate_operations(prev_char, next_char, char)

            new_expression = expression[:i-1] + [result] + expression[i+2:]
            return solve_operations(new_expression, operators)

    return expression


def get_puzzle_numbers(numbers):
    string_numbers = ''.join([str(number) for number in numbers])
    return [int(char) for char in string_numbers]


def get_equation(expression, result):
    str_expression = ''.join([str(x) for x in expression])
    equation = f'{str_expression}={result}'

    return equation

    
main()