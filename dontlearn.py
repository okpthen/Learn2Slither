from Q_table import Q_table
from Board import Board, SNAME_ACTION
from config import Default_sessions
import time


def display(Q, args):
    board = Board(args.size)
    state = board.state()
    duration = 0
    max_length = 3
    if args.step_by_step:
        time.sleep(1)
        board.print_vis()
    while True:
        if args.step_by_step:
            time.sleep(1)
        Q.init_state(state)
        action = Q.max_action(state)
        end, _ = board.action(action)
        if args.step_by_step:
            print(SNAME_ACTION[action])
            if end is False:
                board.print_vis()
        new_state = board.state()
        state = new_state
        if max_length < board.snake_size():
            max_length = board.snake_size()
        duration += 1
        if end:
            print(f"Game over, length = {max_length}, duratio = {duration}")
            break
        if duration > 500:
            print(f"Snake go loop, length = {max_length}")
            break
    return max_length, duration


def dontlearn(args):
    Q = Q_table(args.load)
    max_length = 0
    max_duration = 0
    loop = 0
    if args.sessions == Default_sessions:
        time = 100
    else:
        time = args.sessions
    for _ in range(time):
        length, duration = display(Q, args)
        if duration == 501:
            loop += 1
        if max_length < length:
            max_length = length
            max_duration = duration
    print(f"result,  max length = {max_length}, \
          duration = {max_duration}, loop = {loop}")
