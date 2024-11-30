from Q_table import Q_table
from Board import Board, SNAME_ACTION
from config import Default_sessions
import time
import os

def display(Q, args):
    board = Board(args.size)
    state = board.state()
    duration = 0
    max_length = 3
    if args.step_by_step:
        time.sleep(1)
    if args.visual == "on":
        board.print_vis()
    while True:
        if args.step_by_step:
            time.sleep(1)
        Q.init_state(state)
        action = Q.max_action(state)
        end, _ = board.action(action)
        if args.visual == "on":
            print(SNAME_ACTION[action])
            if end == False:
                board.print_vis()
        new_state = board.state()
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
    if args.sessions == Default_sessions:
        time = 100
    else:
        time = args.sessions
    for _ in range(time):
        length, duration = display(Q, args)
        if max_length < length:
            max_length = length
            max_duration = duration
    print(f"result,  max length = {max_length}, duration = {max_duration}")