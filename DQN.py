import torch
import torch.nn as nn
# import torch.nn.functional as F
# import torch.optim as optim
# import torchvision
# from   torchvision import transforms
from Config import NUM_INPUT, NUM_OUTPUT


class DQN(nn.Module):
    def __init__(self):
        super(DQN, self).__init__()
        # self.fc1 = nn.Linear(NUM_INPUT, 128)
        # self.fc2 = nn.Linear(128, 256)
        # self.fc3 = nn.Linear(256, 256)
        # self.fc4 = nn.Linear(256, 128)
        # self.fc5 = nn.Linear(128, NUM_OUTPUT)
        self.q_net = nn.Sequential(
            nn.Linear(NUM_INPUT, 128),
            nn.Linear(128, 256),
            nn.Linear(256, 256),
            nn.Linear(256, 128),
            nn.Linear(128, NUM_OUTPUT)
        )

    
    def forward(self, x):
        if isinstance(x, list):
            x = torch.tensor(x, dtype=torch.float32)
        return self.q_net(x)