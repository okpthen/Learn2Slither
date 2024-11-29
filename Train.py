from Board import Board
from Config import TARGET_UPDATE_INTERVAL, BATCH_SIZE, DISCOUNT_FACTOR, LEARNING_RATE
from DQN import DQN
from Exploration import Agent
from ReplayBuffer import ReplayBuffer
import torch
import torch.nn as nn
import torch.optim as optim


def tuple_to_tensor(q_values, actions, rewards, new_state, end, states):
    q_values = torch.stack(q_values)
    actions = torch.tensor(actions)
    actions = actions.unsqueeze(1)
    rewards = torch.tensor(rewards)
    new_state = tuple(torch.tensor(state) if isinstance(state, list)\
                       else state for state in new_state)
    new_state = torch.stack(new_state)
    new_state = new_state.float()
    # new_state = torch.stack(new_state)
    end = torch.tensor(end, dtype=torch.bool) 
    return q_values, actions, rewards, new_state, end



def update_policy(policy_net, target_net, replay : ReplayBuffer, optimizer):
    if replay.size() < BATCH_SIZE:
        return
    batch = replay.sample()
    q_values, states, actions, rewards, new_state, end = zip(*batch)

    q_values, actions, rewards, new_state, end = \
        tuple_to_tensor(q_values, actions, rewards, new_state, end, states)
    current_q_values = q_values.gather(1, actions)
    next_max_q_values = target_net(new_state).max(1)[0].detach()
    target_q_values = rewards + (DISCOUNT_FACTOR * next_max_q_values * ~end)

    # current_q_values = torch.tensor(current_q_values, dtype=torch.float32, requires_grad=True)
    # target_q_values = torch.tensor(target_q_values, dtype=torch.float32, requires_grad=True) 

    current_q_values = current_q_values.clone().detach().requires_grad_(True)
    target_q_values = target_q_values.clone().detach().requires_grad_(True)
    target_q_values = target_q_values.unsqueeze(1)

    # loss_fn = nn.MSELoss()
    loss_fn = nn.HuberLoss(delta=1.0)
    loss = loss_fn(current_q_values, target_q_values)
    
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    return (loss)



def train(args):
    policy_net = DQN()
    # target_net = copy.deepcopy(policy_net)
    target_net = DQN()
    replay = ReplayBuffer()
    agent = Agent(args.sessions)
    max_length = 0
    optimizer = optim.Adam(policy_net.parameters(), lr=LEARNING_RATE)
    for i in range(args.sessions):
        board = Board(args.size)
        duration = 1
        if i % TARGET_UPDATE_INTERVAL == 0:
            target_net.load_state_dict(policy_net.state_dict())
            # print(f"update target_net {i}")
        while True:
            state = board.state()
            q_values = policy_net(state)
            action = agent.select_action(q_values, board, i)
            end, reword = board.action(action)
            new_state = board.state()
            replay.add((q_values, state, action, reword, new_state, end))
            # if i % 100 == 0:
            #     update_policy(policy_net, target_net, replay, optimizer)
            
            if end:
                loss = update_policy(policy_net, target_net, replay, optimizer)
                if i % 100000 == 0:
                    # torch.save(policy_net.q_net.state_dict(), f"models/{i}time.pth")
                    # print(f"savint model: models/{i}time.pth")
                    print(f"Max Size {max_length}")
                size = board.snake_size()
                if size > max_length:
                    max_length = size
                # print(f"{i+1}/{args.sessions}\tGame over, max length = {size}, max duration = {duration}")
                if i % 1000 == 0:
                    print(f"{i}/{args.sessions}\tGame over, max length = {size}, loss = {loss}")
                break
            duration += 1
    # torch.save(target_net.q_net.state_dict(), "models/q_net.pth")
    torch.save(target_net.state_dict(), "models/q_net.pth")

    print(f"Result Max Size {max_length}")