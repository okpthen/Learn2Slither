from Board import Board, SNAME_ACTION
from Q_table import Q_table
from config import Learning_Rate, Discount_Factor
from Exploration import Agent

def section(Q : Q_table, args, agent , i):
    board = Board(args.size)
    state = board.state()
    duration = 0
    max_length = 3
    while True:
        Q.init_state(state)
        action = agent.select_action(Q, i, state)
        score_prev = Q[state][action]
        if args.visual == "on":
            board.print_vis()
            print(SNAME_ACTION[action])
            print("\n")
        end, reword = board.action(action)
        new_state = board.state()
        if end:
            tmp = reword - score_prev
        else:
            tmp = (reword + (Discount_Factor * Q.max_point(new_state)) - score_prev)
        Q[state][action] = score_prev + (Learning_Rate * tmp)
        state = new_state
        if max_length < board.snake_size():
            max_length = board.snake_size()
        duration += 1
        if end:
            if args.sessions > 100000:
                if max_length > 24:
                    print(f"{i}/{args.sessions} Game over, max length = {max_length}, max duratio = {duration}")
                elif i % 50000 == 0:
                    print(f"{i}/{args.sessions} Game over, max length = {max_length}, max duratio = {duration}")
            else:
                print(f"{i}/{args.sessions} Game over, max length = {max_length}, max duratio = {duration}")
            break
    return max_length

def train(args):
    Q = Q_table(args.load)
    max = 0
    agent = Agent(args.sessions)
    for i in range (args.sessions):
        length = section(Q, args, agent, i)
        if max < length:
            max = length
    print(f"max length :{max}")
    print(f"Q_table length = {len(Q)}")
    Q.save(args.save)