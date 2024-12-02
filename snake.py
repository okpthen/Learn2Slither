from Args import parse_args
from Test import display_board
from train import train
from dontlearn import dontlearn

if __name__ == "__main__":
    args = parse_args()
    if args.test:
        display_board(args)
    elif args.dontlearn:
        dontlearn(args)
    else:
        train(args)
        # print(f"Visual: {args.visual}")
        # print(f"Load model: {args.load}")
        # print(f"Sessions: {args.sessions}")
        # print(f"Don't Learn: {args.dontlearn}")
        # print(f"Step by Step: {args.step_by_step}")
        # print(f"test: {args.test}")
