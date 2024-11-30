from Q_table import Q_table
from Board import Board, SNAME_ACTION

def display(Q, args):
    board = Board(args.size)
    state = board.__hash__()
    duration = 0
    max_length = 3
    while True:
        Q.init_state(state)
        action = Q.max_action(state)
        # action = board.max_action(Q, state)
        if args.visual == "on":
            board.print_vis()
            print(SNAME_ACTION[action])
            print("\n")
        if SNAME_ACTION[action] == "UP":
            end, _ = board.up()
        elif SNAME_ACTION[action] == "DOWN":
            end, _ = board.down()
        elif SNAME_ACTION[action] == "RIGHT":
            end, _ = board.right()
        elif SNAME_ACTION[action] == "LEFT":
            end, _ = board.left()
        new_state = board.__hash__()
        state = new_state
        if max_length < board.snake_size():
            max_length = board.snake_size()
        duration += 1
        if end:
            print(f"Game over, max length = {max_length}, max duratio = {duration}")
            break
        if duration > 1000:
            print(f"snake go loop ")
            break 
    return max_length, duration


def dontlearn(args):
    Q = Q_table(args.load)
    max_length = 0
    max_duration = 0
    for _ in range(args.sessions):
        length, duration = display(Q, args)
        if max_length < length:
            max_length = length
            max_duration = duration
        # if max_duration < duration and duration < 1000:
        #     max_duration = duration
    print(f"result,  max length = {max_length}, duration = {max_duration}")