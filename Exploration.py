import numpy as np
from Config import EXPLORATION_RATE, EXPLORATION_RATE_DECRACE, EXPLORATION_RATE_MIN
import random

class Agent:
    def __init__(self):
        self.start = EXPLORATION_RATE
        self.end = EXPLORATION_RATE_MIN
        self.rate = EXPLORATION_RATE_DECRACE
        self.step = 0
    
    def get_epsilon(self):
        return max((self.start - self.rate * self.step), self.end)

    def select_action(self, output):
        epsilon = self.get_epsilon()
        self.step += 1
        if np.random.rand() <= epsilon:
            return random.randint(0, 3)
        else:
            print(output)
            return output.argmax().item()