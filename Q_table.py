import random
import pickle
import os
import sys

class Q_table(dict):
    def __init__(self, file):
        if file:
            if os.path.exists(file):
                with open(file, "rb") as f:
                    data = pickle.load(f)
                    super().__init__(data)
            else:
                print(f"{file} doesn't exist.")
                sys.exit()
        else:
            super().__init__()

    def save(self, file_name):
        with open(file_name, "wb") as f:
            pickle.dump(self, f)
        print(f"Save learning state : {file_name}")
        

    def setitem(self, state, action, reword):
        if state in self:
            self[state][action] = reword
        else:
            self[state] = {}
            for i in range(4):
                if i == action:
                    self[state][i] = reword
                else:
                    self[state][i] = 0.0

    def max_action(self, state):
        if state not in self:
            return random.randint(0, 3)
        actions = self[state]
        max_value = max(actions.values())
        max_actions = [action for action, value in actions.items() if value == max_value]
        return random.choice(max_actions)
    
    def max_point(self, state):
        if state not in self:
            return 0.0
        actions = self[state]
        return max(actions.values())
    
    def init_state(self, state):
        if state in self:
            return
        self[state] = {}
        for i in range(4):
            self[state][i] = 0.0

