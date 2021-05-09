class InitiativeStack:
    
    def put_back(self):
        self.stack = []
        for key in self.tokens.keys():
            self.stack.extend([self.tokens[key]] * key)
    
    def reset(self):
        self.tokens: dict = {
            'End of the Round': 1,
            'Enemies': 0,
            'Henchmen': 0
        }
        self.put_back()
    
    def __init__(self):
        # Variable declarations
        self.tokens: dict = {}
        self.stack: list = []
        
        self.reset()
        self.put_back()
    
    def clear(self):
        self.tokens['Enemies'] = 0

    def add_player(self, name):
        self.tokens[name] = 2

    def rmv_player(self, name):
        # Delete the key (catch the KeyError somewhere higher if raised)
        del self.tokens[name]

    def remove_player(self, name):
        return self.tokens.pop(name, None)

st = InitiativeStack()
print(st.tokens)