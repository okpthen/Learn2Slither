from Board import Board, SNAME_ACTION

def display(Q, args):
    board = Board(args.size)
    state = board.__hash__()
    duration = 0
    max_length = 3
    while True:
        if args.visual == "on":
            board.print_vis()
        if max_length < board.snake_size():
            max_length = board.snake_size()
        duration += 1
        if duration > 1000:
            print(f"snake go loop ")
            break 
    return max_length, duration


def dontlearn(args):
    max_length = 0
    max_duration = 0
