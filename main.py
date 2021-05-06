from dice import *
from rpn import *

if __name__ == '__main__':
    conv = Converter('max(3*(2d6+1)-2, 5)')
    ev = Evaluator(conv.convert())
    print(conv.details)
    print(ev.evaluate())
    print(ev.result)