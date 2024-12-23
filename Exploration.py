import numpy as np
from config import EXPLORATION_RATE, EXPLORATION_RATE_MIN
import random

class Agent:
    def __init__(self, size):
        self.start = EXPLORATION_RATE
        self.end = EXPLORATION_RATE_MIN
        self.size = size
        self.slope =  (2 * (self.end - self.start)) / size
    
    def get_epsilon(self, i):
        if i > 0.95 * self.size:
            return 0
        epsilion =  self.start + self.slope * i
        return max(epsilion , self.end)

    def select_action(self, Qtable, i, state):
        epsilon = self.get_epsilon(i)
        if np.random.rand() <= epsilon:
            return random.randint(0, 3)
        else:
            return Qtable.max_action(state)