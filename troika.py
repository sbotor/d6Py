#############################################################
# MAYBE THIS WILL BE DONE SOMEDAY BUT THAT DAY IS NOT TODAY #
#############################################################

from random import choices

class InitiativeStack:
    
    END = 'The End of the Round'
    ENEM = 'Enemies'
    HENCH = 'Henchmen'
    
    def put_back(self):
        for value in self._tokens.values():
            value[0] = value[1]
    
    def reset(self):
        self._tokens: dict = {
            self.END: [1, 1],
            self.ENEM: [0, 0],
            self.HENCH: [0, 0]
        }
        self.put_back()
    
    def __init__(self):
        # Variable declarations
        self._tokens: dict = {}
        
        self.reset()
        self.put_back()
    
    def clear(self):
        # Clear the enemy and henchmen tokens
        self._tokens[self.ENEM] = [0, 0]
        self._tokens[self.HENCH] = [0, 0]
        self.put_back()

    def add_player(self, name):
        if name not in (self.END, self.ENEM, self.HENCH):
            self._tokens[name] = [2, 2]
        else:
            raise ValueError('Invalid character name')

    def rmv_player(self, name):
        if name not in (self.END, self.ENEM, self.HENCH):
            try:
                del self._tokens[name]
            except KeyError:
                raise ValueError('No such character exists')
        else:
            raise ValueError('Invalid character name')

    def __iadd__(self, other):
        self._tokens[self.ENEM][0] += other
        self._tokens[self.ENEM][1] += other
        return self

    def draw(self):
        weights = []
        for value in self._tokens.values():
            weights.append(value[0])

        drawn = choices(list(self._tokens.keys()), weights=weights, k=1)[0]
        if drawn == 'The End of the Round':
            self.put_back()
        else:
            self._tokens[drawn][0] -= 1

        return drawn

    def add_players(self, *args):
        for name in args:
            self.add_player(name)

# Testing
st = InitiativeStack()
st += 12
st.add_players('P1', 'P2', 'P3')
st.put_back()

while True:
    #print(st.stack)
    drawn = st.draw()
    print(drawn, st._tokens)
    
    if drawn == st.END:
        break