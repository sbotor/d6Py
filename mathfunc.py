import math
import statistics

# Function dictionary
funcs = {
    # Misc
    'sqrt': math.sqrt,
    'abs': abs,
    # Max/min, avg
    'max': max,
    'min': min,
    'avg': statistics.mean,
    'mean': statistics.mean,
    # Rounding
    'round': round,
    'floor': math.floor,
    'ceil': math.ceil,
    # Trigonometric
    'sin': math.sin,
    'cos': math.cos,
    'tan': math.tan
}

def is_func(name: str) -> bool:
    return True if name in funcs.keys() else False