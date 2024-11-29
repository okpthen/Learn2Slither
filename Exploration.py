import numpy as np
from Config import EXPLORATION_RATE, EXPLORATION_RATE_DECRACE, EXPLORATION_RATE_MIN
import random

class Agent:
    def __init__(self, size):
        self.start = EXPLORATION_RATE
        self.end = EXPLORATION_RATE_MIN
        self.rate = EXPLORATION_RATE_DECRACE
        self.slope =  (2 * (self.end - self.start)) / size
        self.step = 0
    
    def add_step(self):
        self.step += 1
    
    def get_epsilon(self, i):
        epsilion =  self.start + self.slope * i
        return max(epsilion , self.end)

    def select_action(self, output, board, i):
        epsilon = self.get_epsilon(i)
        # print(epsilon)
        self.step += 1
        if np.random.rand() <= epsilon:
            return random.randint(0, 3)
        else:
            # return output.argmax().item()
            return board.max_action()