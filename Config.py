SCORE_END = -10
SCOER_MOVE = -0.1
SCORE_GREEN = 1.5
SCORE_RED = -2
SCORE_CLEAR = 1000
LEARNING_RATE = 0.001
DISCOUNT_FACTOR = 0.95
EXPLORATION_RATE = 1.0
EXPLORATION_RATE_MIN = 0.1
EXPLORATION_RATE_DECRACE = 0.001
SNAME_ACTION = {
    0: "UP",
    1: "DOWN",
    2: "RIGHT",
    3: "LEFT"
}
BATCH_SIZE = 64
REPLAY_BUFFER_SIZE = 10000
NUM_ACTIONS = 4
NUM_INPUT = 100
NUM_OUTPUT = 4
TARGET_UPDATE_INTERVAL = 10