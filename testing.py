from dice import *
from expr import *

if __name__ == '__main__':
    calc = Calculator('5 / 3')
    calc.calculate()
    print(calc.expression)
    print(calc.details)
    print(calc.result)