import random
from Config import BATCH_SIZE, REPLAY_BUFFER_SIZE
from collections import deque

class ReplayBuffer:
    def __init__(self):
        self.buffer = deque(maxlen=REPLAY_BUFFER_SIZE)
        self.batch_size = BATCH_SIZE
    
    def add (self, experience):
        self.buffer.append(experience)
    
    def sample(self):
        return random.sample(self.buffer, self.batch_size)
    
    def size(self):
        return len(self.buffer)