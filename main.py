from dice import *
from expr import *

if __name__ == '__main__':
    calc = Calculator('max(3*(d6+1)-2, 5)')
    calc.calculate()
    print(calc.expression)
    print(calc.details)
    print(calc.result)