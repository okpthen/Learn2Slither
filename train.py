from Board import Board, SNAME_ACTION
import random
from Q_table import Q_table

Learning_Rate = 0.1
Discount_Factor = 0.95
Exploration_Rate = 1.0
Exploration_Rate_min = 0.1
Exploration_Rate_decrace = 0.001

def section(Q : Q_table, args):
    board = Board(args.size)
    state = board.__hash__()
    duration = 0
    max_length = 3
    Exploration = Exploration_Rate
    while True:
        Q.init_state(state)
        epsilon_greedy = random.randint(1, 1000) / 1000
        if epsilon_greedy <= Exploration:
            # action = Q.max_action(state)
            action = board.max_action(Q, state)
        else:
            action = random.randint(0, 3)
        score_prev = Q[state][action]
        if args.visual == "on":
            board.print_vis()
            print(SNAME_ACTION[action])
            print("\n")
        if SNAME_ACTION[action] == "UP":
            end, reword = board.up()
        elif SNAME_ACTION[action] == "DOWN":
            end, reword = board.down()
        elif SNAME_ACTION[action] == "RIGHT":
            end, reword = board.right()
        elif SNAME_ACTION[action] == "LEFT":
            end, reword = board.left()
        new_state = board.__hash__()
        tmp = (reword + (Discount_Factor * Q.max_point(new_state)) - score_prev)
        Q[state][action] = score_prev + (Learning_Rate * tmp)
        state = new_state
        if max_length < board.snake_size():
            max_length = board.snake_size()
        duration += 1
        if end:
            print(f"Game over, max length = {max_length}, max duratio = {duration}")
            break
    return max_length

def train(args):
    Q = Q_table(args.load)
    max = 0
    for i in range (args.sessions):
        length = section(Q, args)
        if max < length:
            max = length
    print(f"max length :{max}")
    print(f"Q = {len(Q)}")
    # print(args)
    Q.save(args.save)