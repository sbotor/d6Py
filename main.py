from dice import *
from rpn import *

if __name__ == '__main__':
    r = Roller('4d6!kl2')
    r.roll()
    print(r, '\n')
    
    conv = Converter('e^4')
    conv.convert()
    print(conv._tokens)
    print(conv.converted)
    print(conv.details)
    #print(conv._precedence.get('/'))
    #conv.convert()