import re
import dice
from collections import deque
from enum import Enum

class Converter():
    
    # Operator precedence dictionary
    _precedence = {
        # 0
        '+': 0,
        '-': 0,
        # 1
        '*': 1,
        '/': 1,
        '%': 1,
        # 2
        '^': 2,
        # 3
        'n': 3
    }

    # Operator associavity dictionary
    _left_assoc = {
        # Yes
        '+': True,
        '-': True,
        '*': True,
        '/': True,
        '%': True,
        # No
        '^': False,
        'n': False
    }
    
    num_regex = re.compile(r'\d+(\.\d+)?') # Number regex
    dice_regex = dice.Roller.expr_regex # Dice notation regex
    func_regex = re.compile(r'[A-Za-z]{3}[A-Za-z]*') # Function regex
    pi_regex = re.compile(r'[pP][iI]') # Number pi regex
    e_regex = re.compile(r'e|E') # Number e regex

    class TokenType(Enum):

        START = 0
        NUM = 1
        OPER = 2
        R_PAR = 3
        L_PAR = 4
        FUNC = 5

    def __init__(self, expression: str):
        # Variable definitions
        self._expr: str = expression # Input expression
        self._tokens: list = None # A list of tokens to convert, extracted from the expression
        self.pretty_expr: str = None # Pretty cleaned-up expression
        self.converted: str = None # Data converted into RPN
        self._op_stack: deque = deque() # RPN stack
        self._arg_c: deque = deque() # RPN function argument counter stack
        self._prev_token: Converter.TokenType = Converter.TokenType.START # Previous token type
        self.details: str = None # Details including dice rolls

    def clear(self):
        self.pretty_expr = None
        self.converted = None
        self._op_stack = deque()
        self._arg_c = deque()
        self._prev_token = Converter.TokenType.START
        self.details = None
    
    def _prepare(self):
        self._expr = self._expr.replace(' ', '') # Remove spaces
        self._expr = re.sub(r'[\(\)\+\-\*/,\^%]', r' \g<0> ', self._expr) # Divide into tokens by ()+-*/^%,
        self._tokens = self._expr.split()
    
    def _expected(self, token):
        # A number or a function
        if token in (Converter.TokenType.NUM, Converter.TokenType.FUNC):
            pass
    
    def convert(self):
        self._prepare()

        for token in self._tokens:
            
            # The token is a number
            if self.num_regex.match(token):
                pass
            
            # The token can be an operator or e
            elif len(token) == 1:
                pass

            # The token is a die roll
            elif self.dice_regex.match(token):
                pass

            # The token is a function
            elif self.func_regex.match(token):
                pass

            # The token is pi
            elif self.pi_regex.match(token):
                pass

            else:
                raise ValueError('Unexpected token "{}" during conversion'.format(token))
    
        # Check if the last token was a number or right parentesis
        if self._prev_token not in (Converter.TokenType.NUM, Converter.TokenType.R_PAR):
            raise ValueError('Unexpected token "{}" at the end of the expression'.format(token))