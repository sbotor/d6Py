from dice import *
from rpn import *

if __name__ == '__main__':
    r = Roller('4d6!kl2')
    r.roll()
    print(r, '\n')
    
    conv = Converter('1+(2d6-4)*3')
    conv._prepare()
    print(conv._tokens)
    #print(conv._precedence.get('/'))
    #conv.convert()