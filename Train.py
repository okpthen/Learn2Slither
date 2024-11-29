from Board import Board, SNAME_ACTION
import copy
from Config import TARGET_UPDATE_INTERVAL, BATCH_SIZE, DISCOUNT_FACTOR, LEARNING_RATE
from DQN import DQN
from Exploration import Agent
from ReplayBuffer import ReplayBuffer
import torch
import torch.nn as nn
import torch.optim as optim

def tuple_to_tensor(q_values, actions, rewards, new_state, end):
    q_values = torch.stack(q_values)
    actions = torch.tensor(actions)
    actions = actions.unsqueeze(1)
    rewards = torch.tensor(rewards)
    new_state = tuple(torch.tensor(state) if isinstance(state, list)\
                       else state for state in new_state)
    new_state = torch.stack(new_state)
    new_state = new_state.float()
    # new_state = torch.stack(new_state)
    end = torch.tensor(end)
    return q_values, actions, rewards, new_state, end

def update_policy(policy_net, target_net, replay : ReplayBuffer):
    if replay.size() < BATCH_SIZE:
        return
    batch = replay.sample()
    q_values, states, actions, rewards, new_state, end = zip(*batch)

    q_values, actions, rewards, new_state, end = \
        tuple_to_tensor(q_values, actions, rewards, new_state, end)
    current_q_values = q_values.gather(1, actions)
    next_max_q_values = target_net(new_state).max(1)[0].detach()
    target_q_values = rewards + (DISCOUNT_FACTOR * next_max_q_values * ~end)

    # current_q_values = torch.tensor(current_q_values, dtype=torch.float32, requires_grad=True)
    # target_q_values = torch.tensor(target_q_values, dtype=torch.float32, requires_grad=True) 

    current_q_values = current_q_values.clone().detach().requires_grad_(True)
    target_q_values = target_q_values.clone().detach().requires_grad_(True)
    target_q_values = target_q_values.unsqueeze(1)

    loss_fn = nn.MSELoss()
    loss = loss_fn(current_q_values, target_q_values)

    optimizer = optim.Adam(policy_net.parameters(), lr=LEARNING_RATE)
    
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()



def train(args):
    policy_net = DQN()
    # target_net = copy.deepcopy(policy_net)
    target_net = DQN()
    replay = ReplayBuffer()
    for i in range(args.sessions):
        board = Board(args.size)
        duration = 1
        while True:
            agent = Agent()
            state = board.state()
            q_values = policy_net(state)
            action = agent.select_action(q_values)
            board.print_map()
            print(SNAME_ACTION[action])
            end, reword = board.action(action)
            new_state = board.state()
            replay.add((q_values, state, action, reword, new_state, end))
            update_policy(policy_net, target_net, replay)
            if end:
                print(f"{i+1}/{args.sessions}\tGame over, max length = {board.snake_size()}, max duration = {duration}")
                break
            if i % TARGET_UPDATE_INTERVAL == 0:
                target_net.load_state_dict(policy_net.state_dict())
            duration += 1