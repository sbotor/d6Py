import random
import re

# A die class
class Die:
    
    def __init__(self, sides = 6, kept = True):
        self.sides = sides
        if sides <= 0:
            raise ValueError('Incorrect number of sides')
        self.kept = kept
        self.result = None
    
    def __str__(self):
        return str(self.result)

    def __int__(self):
        return self.result
    
    # Less than
    def __lt__(self, other):
        return self.result < other.result

    # Less or equal to
    def __le__(self, other):
        return self.result <= other.result

    # Equal to
    def __eq__(self, other):
        return self.result == other.result

    # Not equal to
    def __ne__(self, other):
        return self.result != other.result

    # Greater than
    def __gt__(self, other):
        return self.result > other.result

    # Greater or equal to
    def __ge__(self, other):
        return self.result >= other.result

    # Roll the die
    def roll(self):
        self.result = random.randint(1, self.sides)
        return self.result

# A dice roll class
class Roller:
    expr_regex = re.compile(r'^(\d+)d(\d+)(!)?((k|d)(h|l)?\d+)?$', re.IGNORECASE)
    
    def __init__(self, expression):
        self.details = None
        self.result = None
        self._dice = None
        match = self.expr_regex.match(expression)
        
        if match:
            groups = match.groups()
            
            self._starting_dice = int(groups[0])
            self._sides = int(groups[1])
            self._exploding = groups[2] != None

            self._keep_info = groups[3] # Save keep/drop info
            if groups[3]:
                if not groups[5]:
                    if groups[4] == 'k':
                        self._keep_info = '{0}h{1}'.format(self._keep_info[0], self._keep_info[1:])
                    elif groups[4] == 'd':
                        self._keep_info = '{0}l{1}'.format(self._keep_info[0], self._keep_info[1:])
                    else:
                        raise ValueError('Inappropriate dice expression')
        else:
            raise ValueError('Inappropriate dice expression')

    def __str__(self):
        return self.details

    def roll(self):
        self._dice = [Die(self._sides) for i in range(self._starting_dice)] # Fill the list of dice
        
        # Roll the dice
        i = 0
        while i < len(self._dice):
            if self._dice[i].roll() == self._sides and self._exploding:
                self._dice.insert(i + 1, Die(self._sides))
            i += 1
        
        # Add the dice together
        self.result = 0
        for d in self._dice:
            if d.kept:
                self.result += d.result

        # Fetch details
        self.details = str(self.result) + '['
        first = True
        for d in self._dice:
            # Skip the plus sign if the die is the first one
            if not first:
                self.details += '+'
            else:
                first = False
            
            # Check if the die is kept
            if not d.kept:
                self.details += '#'

            # Add the die's result
            self.details += str(d)
            # Check if the die exploded
            if self._exploding and d.result == d.sides:
                self.details += '!'

        self.details += ']'

        return self.result