import argparse
from config import Default_size, Default_save, Default_sessions


def parse_args():
    parser = argparse.ArgumentParser(
        description="Snake Game with customizable settings.")
    parser.add_argument('-visual', choices=['on', 'off'], default='off',
                        help="Enable or disable visual display (default: off)")
    parser.add_argument('-load', type=str,
                        help="Path to the trained model file to load.")
    parser.add_argument('-sessions', type=int, default=Default_sessions,
                        help="Number of game sessions to play (default: 1).")
    parser.add_argument('-dontlearn', action='store_true',
                        help="Disable learning during the game.")
    parser.add_argument('-step-by-step', action='store_true',
                        help="Enable step-by-step mode for debugging.")
    parser.add_argument('-test', action='store_true',
                        help="debud")
    parser.add_argument('-size', default=Default_size, type=int,
                        help="Grid size (defaul 10)")
    parser.add_argument('-save', default=Default_save, type=str,
                        help='Q tabele data (default: models/q_table.pkl)')
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    print(f"Visual: {args.visual}")
    print(f"Load model: {args.load}")
    print(f"Sessions: {args.sessions}")
    print(f"Don't Learn: {args.dontlearn}")
    print(f"Step by Step: {args.step_by_step}")
