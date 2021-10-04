import math
import statistics

# Function dictionary
funcs = {
    # Misc
    'sqrt': (math.sqrt, '1'),
    'abs': (abs, '1'),
    # Max/min, avg
    'max': (max, '1+'),
    'min': (min, '1+'),
    'avg': (statistics.mean, '1+'),
    'mean': (statistics.mean, '1+'),
    # Rounding
    'round': (round, '1'),
    'floor': (math.floor, '1'),
    'ceil': (math.ceil, '1'),
    # Trigonometric (working weirdly, probably due to floating point precision error)
    #'sin': (math.sin, '1'),
    #'cos': (math.cos, '1'),
    #'tan': (math.tan, '1')
}

def is_func(name):
    return True if name in funcs.keys() else False

def func(name, arg_list):
    found = funcs.get(name, False)
    if found:
        # Single argument functions
        if found[1] == '1' and len(arg_list) == 1:
            return found[0](arg_list[0])
        # Multiple argument functions
        elif found [1] != '1' and len(arg_list) > 0:
            return found[0](arg_list)
        else:
            raise ValueError(f'Incorrect number of arguments ({len(arg_list)}, {found[1]} expected) in function "{name}"')
    else:
        raise ValueError(f'Function "{name}" not found')