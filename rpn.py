from collections import deque
from enum import Enum
import math

import re
import dice
import mathfunc

_NEGATION = 'n'

_num_regex = re.compile(r'^\d+(\.\d+)?$') # Number regex
_dice_regex = dice.Roller.expr_regex # Dice notation regex

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
        _NEGATION: 3
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
        _NEGATION: False
    }
    
    _func_regex = re.compile(r'^[A-Za-z]{3}[A-Za-z]*$') # Function regex
    _pi_regex = re.compile(r'^[pP][iI]$') # Number pi regex
    _e_regex = re.compile(r'^e|E$') # Number e regex

    class TokenType(Enum):

        START = 0 # The beginning
        NUM = 1 # A number or a die
        OPER = 2 # An operator or a comma
        R_PAR = 3 # A right parenthesis
        L_PAR = 4 # A left parenthesis
        FUNC = 5 # A function name
        NEG = 6 # Negation

    def __init__(self, expression: str = ''):
        # Variable definitions
        self.expression: str = expression # Input expression
        self.converted: str = '' # Data converted into RPN
        self.details: str = '' # Details including dice rolls

        self._data: str = '' # Expression used in converting
        self._tokens: list = [] # A list of tokens to convert, extracted from the data
        self.pretty_expr: str = '' # Pretty cleaned-up expression
        self._output_list: list = [] # Output list that will be converted into the converted string
        self._details_list: list = [] # A list of details to be converted into the details string
        self._op_stack: deque = deque() # RPN stack
        self._arg_c: deque = deque() # RPN function argument counter stack
        self._prev_token: Converter.TokenType = Converter.TokenType.START # Previous token type

    def clear(self):
        self.pretty_expr = ''
        self._data = ''
        self.converted = ''
        self._output_list = []
        self._details_list = []
        self._op_stack = deque()
        self._arg_c = deque()
        self._prev_token = Converter.TokenType.START
        self.details = ''
    
    def _prepare(self):
        self._data = self.expression.replace(' ', '') # Remove spaces
        self._data = re.sub(r'[\(\)\+\-\*/,\^%]', r' \g<0> ', self._data) # Divide into tokens by ()+-*/^%,
        self._tokens = self._data.split()
    
    def _expected(self, token) -> bool:
        # A number or a function
        if token in (Converter.TokenType.NUM, Converter.TokenType.FUNC):
            return self._prev_token in (Converter.TokenType.START, Converter.TokenType.OPER, Converter.TokenType.L_PAR, Converter.TokenType.NEG)
        
        # A binary operator, right parenthesis or comma
        elif token in (Converter.TokenType.R_PAR, Converter.TokenType.OPER):
            return self._prev_token in (Converter.TokenType.NUM, Converter.TokenType.R_PAR)
        
        # Negation
        elif token == Converter.TokenType.NEG:
            return self._prev_token in (Converter.TokenType.START, Converter.TokenType.L_PAR)
        
        # Left parenthesis
        elif token == Converter.TokenType.L_PAR:
            return self._prev_token in (Converter.TokenType.START, Converter.TokenType.FUNC, Converter.TokenType.OPER, Converter.TokenType.NEG)
        
        else:
            return False
    
    def _pop_out(self):
        if mathfunc.is_func(self._op_stack[-1]):
            self._op_stack[-1] += self._arg_c.pop() # Add the number of arguments to the function's name

        self._output_list.append(self._op_stack.pop())

    def _pop_paren(self):
        # Pop everything until a left parenthesis is encountered
        while self._op_stack and self._op_stack[-1] != '(':
            self._pop_out()

        if not self._op_stack:
            raise ValueError('Mismatched parentheses')

        # Pop the '('
        if self._op_stack[-1] == '(':
            self._op_stack.pop()
        
        # If there is a function at the top pop it
        if mathfunc.is_func(self._op_stack[-1]):
            self._pop_out()

    def _pop_arg(self):
        pass

    def _add_operator(self, operator: str):
        # Pop operators from the top of the stack as long as
        # - they have higher or equal precedence,
        # - aren't the left parenthesis,
        # - are left associative,
        # - the stack is not empty
        while self._op_stack and self._op_stack[-1] != '(' and self._precedence[self._op_stack[-1]] >= self._precedence[operator] and self._left_assoc[operator]:
            self._pop_out()
        
        # Add the operator passed as the argument
        self._op_stack.append(operator)
    
    def _add_function(self, name: str):
        self._op_stack.append(name)
        self._arg_c.append(1)
    
    def convert(self, expression: str = None) -> str:
        if expression != None:
            self.expression = expression
        
        if not self.expression:
            raise ValueError('The expression to convert is empty')
        
        self.clear()
        self._prepare()

        # Iterate over all the tokens
        for token in self._tokens:
            
            # The token is a number
            if _num_regex.match(token):
                if self._expected(Converter.TokenType.NUM):
                    self._output_list.append(str(token)) # Add to output
                    self._details_list.append(str(token)) # Add to details
                    self._prev_token = Converter.TokenType.NUM
            
            # The token can be an operator or e
            elif len(token) == 1:
                # Regular operators
                if token in '+*/^%' and self._expected(Converter.TokenType.OPER):
                    self._add_operator(str(token)) # Add the operator
                    self._details_list.append(f' {str(token)} ') # Add it to the details
                    self._prev_token = Converter.TokenType.OPER
                
                # Difference or negation
                elif token == '-':
                    # Binary operator
                    if self._expected(Converter.TokenType.OPER):
                        self._add_operator(str(token))
                        self._details_list.append(f' {str(token)} ')
                        self._prev_token = Converter.TokenType.OPER
                    # Negation
                    elif self._expected(Converter.TokenType.NEG):
                        self._add_operator(_NEGATION)
                        self._details_list.append('-')
                        self._prev_token = Converter.TokenType.NEG
                    else:
                        raise ValueError(f'Unexpected token "{token}" during conversion')
                
                # Left parenthesis
                elif token == '(' and self._expected(Converter.TokenType.L_PAR):
                    self._op_stack.append(token)
                    self._details_list.append(token)
                    self._prev_token = Converter.TokenType.L_PAR
                
                # Right parenthesis
                elif token == ')' and self._expected(Converter.TokenType.R_PAR):
                    self._pop_paren()
                    self._details_list.append(str(token))
                    self._prev_token = Converter.TokenType.R_PAR
                
                # Comma
                elif token ==',' and self._expected(Converter.TokenType.OPER):
                    self._pop_arg() # Pop the previous sub-expression
                    self._arg_c[-1] += 1 # Increment the argument counter for the current function
                    self._details_list.append(str(token))
                    self._prev_token = Converter.TokenType.OPER
                
                # Number e
                elif self._e_regex.match(token) and self._expected(Converter.TokenType.NUM):
                    self._output_list.append(str(math.e))
                    self._details_list.append(str(math.e))
                    self._prev_token = Converter.TokenType.NUM

            # The token is a die roll
            elif _dice_regex.match(token) and self._expected(Converter.TokenType.NUM):
                r = dice.Roller(token)
                self._output_list.append(str(r.roll()))
                self._details_list.append(r.details)
                self._prev_token = Converter.TokenType.NUM

            # The token is a function
            elif self._func_regex.match(token) and self._expected(Converter.TokenType.FUNC) and mathfunc.is_func(token.lower()):
                self._add_function(token.lower())
                self._prev_token = Converter.TokenType.FUNC

            # The token is pi
            elif self._pi_regex.match(token):
                self._output_list.append(str(math.pi))
                self._details_list.append(str(math.pi))
                self._prev_token = Converter.TokenType.NUM

            else:
                raise ValueError(f'Unexpected token "{token}" during conversion')
    
        # Check if the last token was a number or right parenthesis
        if self._prev_token not in (Converter.TokenType.NUM, Converter.TokenType.R_PAR):
            raise ValueError(f'Unexpected token "{token}" at the end of the expression')
        
        # Pop the rest of the stack and check if parentheses mismatched
        while self._op_stack:
            if self._op_stack[-1] in ('(', ')'):
                raise ValueError('Mismatched parentheses')
            
            self._pop_out()
        
        # Create the output and return it
        self.converted = ' '.join(self._output_list)
        self.details = ''.join(self._details_list)
        return self.converted

class Evaluator():

    _func_regex = re.compile(r'^[A-Za-z]{3}[A-Za-z]*$') # Function regex

    def __init__(self):
        pass