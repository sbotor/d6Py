import random
import re

# A die class
class Die:
    
    def __init__(self, sides = 6, keep = True):
        if sides < 2:
            raise ValueError('Invalid number of sides')

        # Variable declarations
        self.sides: int = sides # How many sides
        self.keep: bool = keep # Should the die be kept in a roll
        self.result: int = None # The result
    
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
        if self.sides > 1:
            self.result = random.randint(1, self.sides)
            return self.result
        else:
            raise ValueError('Invalid number of sides')

# A dice roll class
class Roller:
    
    # Dice roll regex
    _dice_regex = re.compile(r'^(\d+)?d(\d+)(!)?((k|d)(h|l)?(\d+))?$', re.IGNORECASE)
    
    def __init__(self, expression: str):
        # Variable declarations
        self.details: str = '' # Roll details
        self.result: int = None # Roll result
        self._dice: list = [] # List of appropriate Dice objects
        self._starting_dice: int = None # Number of starting dice
        self._sides: int = None # Number of sides of dice to roll
        self._exploding: bool = None # Whether the dice can explode
        self._keep_info: tuple = None # Tuple of (string, string, int) ([k]eep/[d]rop, [h]igh/[l]ow, how_many)
    
        
        match = self._dice_regex.match(expression)
        
        # Extract data from the expression
        if match:
            
            #groups = match.groups()
            
            self._starting_dice = int(match[1]) if match[1] else 1
            self._sides = int(match[2])
            self._exploding = match[3] != None

            # Save keep/drop info
            if match[4]:
                keep_info = [match[5].lower(), match[6], int(match[7])]
                
                # Check if keep/drop number is appropriate
                if keep_info[2] > self._starting_dice:
                    raise ValueError('Invalid number of keep/drop dice')
                
                # Check if k# or d# shorthand used
                if not keep_info[1]:
                    keep_info[1] = 'h' if keep_info[0] == 'k' else 'l'
                    self._keep_info = tuple(keep_info)
                else:
                    # Convert to lowercase for convenience
                    self._keep_info = (keep_info[0], keep_info[1].lower(), keep_info[2])
        else:
            raise ValueError('Invalid dice expression')

    def __str__(self) -> str:
        return self.details

    def __len__(self) -> int:
        return len(self._dice)

    def _keep(self):
        # Find the list of dice to keep
        keep = sorted(self._dice)[-self._keep_info[2]:] if self._keep_info[1] == 'h' else sorted(self._dice)[:self._keep_info[2]]

        # Flag all dice as to drop
        for d in self._dice:
            d.keep = False
        
        # Flag the kept dice
        for d in self._dice:
            if d in keep:
                d.keep = True
                keep.remove(d)

    def _drop(self):
        # Find the list of all dice to drop
        drop = sorted(self._dice)[-self._keep_info[2]:] if self._keep_info[1] == 'h' else sorted(self._dice)[:self._keep_info[2]]

        # Flag all the dice as to keep
        for d in self._dice:
            d.keep = True
        
        # Flag the kept dice
        for d in self._dice:
            if d in drop:
                d.keep = False
                drop.remove(d)

    def roll(self) -> int:
        self._dice = [Die(self._sides) for i in range(self._starting_dice)] # Fill the list of dice
        
        # Roll the dice
        i = 0
        while i < len(self._dice):
            if self._dice[i].roll() == self._sides and self._exploding: # Check if exploded if possible
                self._dice.insert(i + 1, Die(self._sides))
            i += 1
        
        if self._keep_info:
            if self._keep_info[0] == 'k':
                self._keep()
            elif self._keep_info[0] == 'd':
                self._drop()
        
        # Add the dice together
        self.result = 0
        for d in self._dice:
            if d.keep:
                self.result += d.result

        # Fetch details
        to_add = [str(self.result) + '[']
        
        first = True
        for d in self._dice:
            # Skip the plus sign if the die is the first one
            if not first:
                to_add.append('+')
            else:
                first = False
            
            # Check if the die is not kept
            if not d.keep:
                to_add.append('#')

            # Add the die's result
            to_add.append(str(d))
            # Check if the die exploded and ! if it did
            if self._exploding and d.result == d.sides:
                to_add.append('!')

        to_add.append(']')
        self.details = ''.join(to_add)

        return self.result