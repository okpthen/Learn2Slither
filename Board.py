from Coordinates import Coordinates
import random
import sys
import hashlib
import copy
from Q_table import Q_table
from config import SCORE_END, SCOER_MOVE, SCORE_GREEN, SCORE_RED, SCORE_CLEAR, SNAME_ACTION


# SNAME_ACTION = {
#     0: "UP",
#     1: "DOWN",
#     2: "RIGHT",
#     3: "LEFT"
# }

END_GAME = True
CONTINUE_GAME = False
# SCORE_END = -100
# SCOER_MOVE = -0.1
# SCORE_GREEN = 5
# SCORE_RED = -5
# SCORE_CLEAR = 1000

class Board:
    """Board class"""
    def __init__(self, size):
        """init board"""
        self.red_apple = Coordinates()
        self.green_apple = [Coordinates(), Coordinates()]
        self.snake_head = Coordinates()
        self.snake_body = []
        self.visibility = []
        self.size = size
        self.make_snake()
        while True:
            self.random()
            if self.check():
                break
        self.make_visibility()

    def __repr__(self):
        """repr"""
        res = "Board State:\n"
        res += f"Red Apple:  {repr(self.red_apple)}\n"
        res += f"Green Apple 1:  {repr(self.green_apple[0])}\n"
        res += f"Green Apple 2:  {repr(self.green_apple[1])}\n"
        res += f"Snake Head :  {repr(self.snake_head)}\n"
        res += f"Snake Body :  {[repr(seg) for seg in self.snake_body]}\n"
        res += "Snake visibility\n"
        res += f"Visibility : {[repr(segment) for segment in self.visibility]}"
        return res

    def __hash__(self):
        self.update_vis()
        # return hash((self.snake_head.x, self.snake_head.y, tuple(
        #     tuple(sorted(segment.items())) for segment in self.visibility
        # )))
        data = f"{self.snake_head.x},{self.snake_head.y}," + "|".join(
            ",".join(f"{k}:{v}" for k, v in sorted(segment.items()))
            for segment in self.visibility
        )
        hash_object = hashlib.sha256(data.encode())
        return int(hash_object.hexdigest(), 16)


    def random(self):
        """init randam"""
        self.red_apple.random(self.size)
        self.green_apple[0].random(self.size)
        self.green_apple[1].random(self.size)

    def check(self):
        """check dup"""
        all_objects = [*self.green_apple, self.red_apple,
                       self.snake_head, *self.snake_body]
        return len(all_objects) == len(set((obj.x, obj.y)
                                           for obj in all_objects))

    def check_new_head(self, new_head):
        all_objcs = [*self.snake_body, new_head]
        return len(all_objcs) == len(set((obj.x, obj.y) for obj in all_objcs))
    
    def make_snake(self):
        """init snake"""
        self.snake_head.random(self.size)
        for _ in range(2):
            while True:
                current_position = self.snake_head
                direction = random.randint(0, 3)
                if SNAME_ACTION[direction] == "UP":
                    if current_position.y == 0:
                        continue
                    new_head = Coordinates(current_position.x,
                                           current_position.y - 1)
                elif SNAME_ACTION[direction] == "DOWN":
                    if current_position.y == 9:
                        continue
                    new_head = Coordinates(current_position.x,
                                           current_position.y + 1)
                elif SNAME_ACTION[direction] == "RIGHT":
                    if current_position.x == 9:
                        continue
                    new_head = Coordinates(current_position.x + 1,
                                           current_position.y)
                elif SNAME_ACTION[direction] == "LEFT":
                    if current_position.x == 0:
                        continue
                    new_head = Coordinates(current_position.x - 1,
                                           current_position.y)
                if self.check_new_head(new_head):
                    self.snake_body.append(self.snake_head)
                    self.snake_head = new_head
                    break

    def print_map(self):
        # GREEN = "\033[32m"
        # RED = "\033[31m"
        # BLUE = "\033[34m"
        RESET = "\033[0m"
        GREEN_T = "\033[42m"
        RED_T = "\033[41m"
        BLUE_T = "\033[44m"
        str = ""
        # str += "WWWWWWWWWWWW\n"
        for y in range(self.size):
            # str += "W"
            for x in range(self.size):
                if self.red_apple.eq(x, y):
                    str += RED_T + "R" + RESET
                elif any(apple.eq(x, y) for apple in self.green_apple):
                    str += GREEN_T + "G" + RESET
                elif self.snake_head.eq(x, y):
                    str += BLUE_T + "H" + RESET
                elif any(body.eq(x, y) for body in self.snake_body):
                    str += BLUE_T + " " + RESET
                else:
                    str += "0"
            # str += "W\n"
            str += "\n"
        # str += "WWWWWWWWWWWW"
        print(str)

    def up(self):
        if self.snake_head.y == 0:
            return END_GAME, SCORE_END
        next_position = Coordinates(self.snake_head.x, self.snake_head.y - 1)
        return self.move(next_position)

    def down(self):
        if self.snake_head.y == self.size -1:
            return END_GAME, SCORE_END
        next_position = Coordinates(self.snake_head.x, self.snake_head.y + 1)
        return self.move(next_position)

    def right(self):
        if self.snake_head.x == self.size - 1:
            return END_GAME, SCORE_END
        next_position = Coordinates(self.snake_head.x + 1, self.snake_head.y)
        return self.move(next_position)

    def left(self):
        if self.snake_head.x == 0:
            return END_GAME, SCORE_END
        next_position = Coordinates(self.snake_head.x - 1, self.snake_head.y)
        return self.move(next_position)

    def move(self, next_position):
        if next_position == self.red_apple:
            return self.conllision_red(next_position)
        for i in range(2):
            if next_position == self.green_apple[i]:
                return self.conllision_green(next_position, i)
        for body in self.snake_body:
            if body == next_position:
                return END_GAME, SCORE_END
        self.snake_body.append(self.snake_head)
        self.snake_head = next_position
        self.snake_body.pop(0)
        return CONTINUE_GAME, SCOER_MOVE

    def conllision_red(self, next_position):
        if len(self.snake_body) == 0:
            return END_GAME, SCORE_END
        self.snake_body.append(self.snake_head)
        self.snake_body.pop(0)
        self.snake_body.pop(0)
        self.snake_head = next_position
        num = 0
        while True:
            num += 1
            if num == 1000:
                print("red")
                self.print_map()
                print(self)
                sys.exit()
            tmp = Coordinates()
            tmp.random(self.size)
            # if self.red_apple == tmp:
            #     continue
            self.red_apple = tmp
            if self.check():
                break
        return CONTINUE_GAME, SCORE_RED

    def conllision_green(self, next_position, i):
        self.snake_body.append(self.snake_head)
        self.snake_head = next_position
        if self.snake_size() == (self.size * 4) - 3:
            return END_GAME, SCORE_CLEAR
        num = 0
        while True:
            num += 1
            if num == 1000:
                print("green")
                self.print_map()
                print(self)
                sys.exit()
            tmp = Coordinates()
            tmp.random(self.size)
            # if self.green_apple[i] == tmp:
            #     continue
            self.green_apple[i] = tmp
            if self.check():
                break
        return CONTINUE_GAME, SCORE_GREEN

    def make_visibility(self):
        if self.snake_head.x == self.red_apple.x or\
                self.snake_head.y == self.red_apple.y:
            self.visibility.append({'R': self.red_apple})
        for apple in self.green_apple:
            if apple.x == self.snake_head.x or apple.y == self.snake_head.y:
                self.visibility.append({'G': apple})
        for body in self.snake_body:
            if body.x == self.snake_head.x or body.y == self.snake_head.y:
                self.visibility.append({'B': body})
        self.visibility.sort(key=lambda segment: sorted(segment.items()))

    def add_char(self, x, y):
        if self.snake_head.eq(x, y):
            return "H"
        for tmp in self.visibility:
            for kye, value in tmp.items():
                if value.eq(x, y):
                    return kye
        if x == self.snake_head.x or y == self.snake_head.y:
            return "0"
        return " "

    def print_vis(self):
        str = ""
        for y in range(10):
            for x in range(10):
                str += self.add_char(x, y)
            str += "\n"
        print(str)

    def update_vis(self):
        self.visibility.clear()
        self.make_visibility()
    
    def snake_size(self):
        return 1 + len(self.snake_body)
    
    def max_action(self, Q : Q_table, state):
        top = -1001
        action = -1
        move_list = []
        for i in range(4):
            tmp = copy.deepcopy(self)
            if i == 0:
                _, score = tmp.up()
                if score > top:
                    top = score
                    action = i
                if score == SCOER_MOVE:
                    move_list.append(i)
                if score == SCORE_END:
                    Q[state][i] == SCORE_END
            elif i == 1:
                _, score = tmp.down()
                if score > top:
                    top = score
                    action = i
                if score == SCOER_MOVE:
                    move_list.append(i)
                if score == SCORE_END:
                    Q[state][i] == SCORE_END
            elif i == 2:
                _, score = tmp.right()
                if score > top:
                    top = score
                    action = i
                if score == SCOER_MOVE:
                    move_list.append(i)
                if score == SCORE_END:
                    Q[state][i] == SCORE_END
            elif i == 3:
                _, score = tmp.left()
                if score > top:
                    top = score
                    action = i
                if score == SCOER_MOVE:
                    move_list.append(i)
                if score == SCORE_END:
                    Q[state][i] == SCORE_END
        if top != SCOER_MOVE:
            return action

        for apple in self.green_apple:
            if apple.x == self.snake_head.x:
                if apple.y > self.snake_head.y and 1 in move_list:
                    return 1
                elif apple.y < self.snake_head.y and 0 in move_list:
                    return 0
            if apple.y == self.snake_head.y:
                if apple.x > self.snake_head.x and 2 in move_list:
                    return 2
                elif apple.x < self.snake_head.x and 3 in move_list:
                    return 3
        for i in range(100):
            action = Q.max_action(state)
            if action in move_list:
                return action
        return action
    