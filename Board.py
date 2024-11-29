from Coordinates import Coordinates
import random
import sys
from Config import SCORE_END, SCOER_MOVE, SCORE_GREEN, SCORE_RED, SCORE_CLEAR, SNAME_ACTION, NUM_INPUT
# import numpy as np
import copy

# SNAME_ACTION = {
#     0: "UP",
#     1: "DOWN",
#     2: "RIGHT",
#     3: "LEFT"
# }

END_GAME = True
CONTINUE_GAME = False

class Board:
    """Board class"""
    def __init__(self, size):
        """init board"""
        self.red_apple = Coordinates()
        self.green_apple = [Coordinates(), Coordinates()]
        self.snake_head = Coordinates()
        self.snake_body = []
        self.visibility_vertical = ""
        self.visibility_horizontal = ""
        self.size = size
        self.make_snake()
        while True:
            self.random()
            if self.check():
                break
        self.make_visibility()

    def __repr__(self):
        """repr"""
        self.make_visibility()
        res = "Board State:\n"
        res += f"Red Apple:  {repr(self.red_apple)}\n"
        res += f"Green Apple 1:  {repr(self.green_apple[0])}\n"
        res += f"Green Apple 2:  {repr(self.green_apple[1])}\n"
        res += f"Snake Head :  {repr(self.snake_head)}\n"
        res += f"Snake Body :  {[repr(seg) for seg in self.snake_body]}\n"
        res += "Snake visibility\n"
        res += f"visibility_vertical: {self.visibility_vertical} {len(self.visibility_vertical)}\n"
        res += f"visibility_horizontal: {self.visibility_horizontal} {len(self.visibility_horizontal)}"
        return res


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
        RESET = "\033[0m"
        GREEN_T = "\033[42m"
        RED_T = "\033[41m"
        BLUE_T = "\033[44m"
        str = ""
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
            str += "\n"
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
        vertical = "W"
        horizontal = "W"
        for i in range (10):
            if self.snake_head.x == self.red_apple.x and self.red_apple.y == i:
                vertical += "R"
            if self.snake_head.y == self.red_apple.y and self.red_apple.x == i:
                horizontal += "R"
            if self.snake_head.y == i:
                vertical += "H"
            if self.snake_head.x == i:
                horizontal += "H"
            for apple in self.green_apple:
                if apple.x == self.snake_head.x and apple.y == i:
                    vertical += "G"
                if apple.y == self.snake_head.y and apple.x == i:
                    horizontal += "G"
            for body in self.snake_body:
                if body.x == self.snake_head.x and body.y == i:
                    vertical += "B"
                if body.y == self.snake_head.y and body.x == i:
                    horizontal += "B"
            if len(vertical) == i + 1:
                vertical += "0"
            if len(horizontal) == i + 1:
                horizontal += "0"
        horizontal += "W"
        vertical += "W"
        self.visibility_vertical = vertical
        self.visibility_horizontal = horizontal

    def add_char(self, x, y):
        if x - 1 == self.snake_head.x:
            return self.visibility_vertical[y]
        if y - 1 == self.snake_head.y:
            return self.visibility_horizontal[x]
        if x == 0 or x == 11 or y == 0 or y == 11:
            return " "
        return "."

    def print_vis(self):
        str = ""
        self.make_visibility()
        for y in range(12):
            for x  in range(12):
                str += self.add_char(x, y)
            str += "\n"
        print(str)
    
    def snake_size(self):
        return 1 + len(self.snake_body)
    
    # def state(self):
    #     # N_L = [False, False, False, False, True]
    #     # B_L = [False, False, False, True, False]
    #     # R_L = [False, False, True, False, False]
    #     # G_L = [False, True, False, False, False]
    #     # H_L = [True, False, False, False, False]
    #     N_L = [False, False, False]
    #     B_L = [False, False, True]
    #     R_L = [False, True, False]
    #     G_L = [False, True, True]
    #     H_L = [True, False, False]
    #     array = []
    #     # array = np.zeros(60, dtype=bool)
    #     self.make_visibility()
    #     for i in range(1, 11):
    #         if self.visibility_horizontal[i] == "0":
    #             array += N_L
    #         elif self.visibility_horizontal[i] == "H":
    #             array += H_L
    #         elif self.visibility_horizontal[i] == "G":
    #             array += G_L
    #         elif self.visibility_horizontal[i] == "R":
    #             array += R_L
    #         elif self.visibility_horizontal[i] == "B":
    #             array += B_L
    #     for i in range(1, 11):
    #         if self.visibility_vertical[i] == "0":
    #             array += N_L
    #         elif self.visibility_vertical[i] == "H":
    #             array += H_L
    #         elif self.visibility_vertical[i] == "G":
    #             array += G_L
    #         elif self.visibility_vertical[i] == "R":
    #             array += R_L
    #         elif self.visibility_vertical[i] == "B":
    #             array += B_L
    #     return array
    
    def reset(self):
        self.snake_body.clear()
        self.make_snake()
        while True:
            self.random()
            if self.check():
                break
        self.make_visibility()

    def action(self, action):
        if SNAME_ACTION[action] == "UP":
            return self.up()
        elif SNAME_ACTION[action] == "DOWN":
            return self.down()
        elif SNAME_ACTION[action] == "RIGHT":
            return self.right()
        elif SNAME_ACTION[action] == "LEFT":
            return self.left()
        
    def state(self):
        # size = 17
        # state = [self.size + 1] * size
        # state[4 * 0 + 0] = self.snake_head.y + 1
        # state[4 * 0 + 1] = self.size - self.snake_head.y
        # state[4 * 0 + 2] = self.size - self.snake_head.x
        # state[4 * 0 + 3] = self.snake_head.y + 1
        # for apple in self.green_apple:
        #     if self.snake_head.x == apple.x:
        #         if apple.y - self.snake_head.y:
        #             if state[4 * 1 + 0] > apple.y - self.snake_head.y:
        #                 state[4 * 1 + 0] = apple.y - self.snake_head.y
        #             elif state[4 * 1 + 1] > self.snake_head.y - apple.y:
        #                 state[4 * 1 + 1] = self.snake_head.y - apple.y
        #     if self.snake_head.y == apple.y:
        #         if apple.x - self.snake_head.x:
        #             if state[4 * 1 + 2] > apple.x - self.snake_head.x:
        #                 state[4 * 1 + 2] = apple.x - self.snake_head.x
        #             elif state[4 * 1 + 3] > self.snake_head.x - apple.x:
        #                 state[4 * 1 + 3] = self.snake_head.x - apple.x
        # if self.snake_head.x == self.red_apple.x:
        #     if self.red_apple.y - self.snake_head.y:
        #         state[4 * 2 + 0] = self.red_apple.y - self.snake_head.y
        #     else:
        #         state[4 * 2 + 1] = self.snake_head.y - self.red_apple.y
        # if self.snake_head.y == self.red_apple.y:
        #     if self.red_apple.x - self.snake_head.x:
        #         state[4 * 2 + 2] = self.red_apple.x - self.snake_head.x
        #     else:
        #         state[4 * 2 + 3] = self.snake_head.x - self.red_apple.x
        # for body in self.snake_body:
        #     if self.snake_head.x == body.x:
        #         if body.y - self.snake_head.y:
        #             if state[4 * 3 + 0] > body.y - self.snake_head.y:
        #                 state[4 * 3+ 0] = body.y - self.snake_head.y
        #             elif state[4 * 3 + 1] > self.snake_head.y - body.y:
        #                 state[4 * 3 + 1] = self.snake_head.y - body.y
        #     if self.snake_body.y == body.y:
        #         if body.x - self.snake_head.x:
        #             if state[4 * 3 + 2] > body.x - self.snake_head.x:
        #                 state[4 * 3 + 2] = body.x - self.snake_head.x
        #             elif state[4 * 3 + 3] > self.snake_head.x - body.x:
        #                 state[4 * 3 + 3] = self.snake_head.x - body.x
        # state[16] = self.snake_size()
        size = NUM_INPUT
        state = [-10] * size
        state[4 * 0 + 0] = self.snake_head.y + 1
        state[4 * 0 + 1] = self.size - self.snake_head.y
        state[4 * 0 + 2] = self.size - self.snake_head.x
        state[4 * 0 + 3] = self.snake_head.x + 1

        for apple in self.green_apple:
            if self.snake_head.x == apple.x:
                distance_y = apple.y - self.snake_head.y
                if distance_y > 0:
                    state[4 * 1 + 0] = min(state[4 * 1 + 0], distance_y)
                elif distance_y < 0:
                    state[4 * 1 + 1] = min(state[4 * 1 + 1], -distance_y)

            if self.snake_head.y == apple.y:
                distance_x = apple.x - self.snake_head.x
                if distance_x > 0:
                    state[4 * 1 + 2] = min(state[4 * 1 + 2], distance_x)
                elif distance_x < 0:
                    state[4 * 1 + 3] = min(state[4 * 1 + 3], -distance_x)

        if self.snake_head.x == self.red_apple.x:
            distance_y = self.red_apple.y - self.snake_head.y
            if distance_y > 0:
                state[4 * 2 + 0] = distance_y
            elif distance_y < 0:
                state[4 * 2 + 1] = -distance_y

        if self.snake_head.y == self.red_apple.y:
            distance_x = self.red_apple.x - self.snake_head.x
            if distance_x > 0:
                state[4 * 2 + 2] = distance_x
            elif distance_x < 0:
                state[4 * 2 + 3] = -distance_x

        for body in self.snake_body:
            if self.snake_head.x == body.x:
                distance_y = body.y - self.snake_head.y
                if distance_y > 0:
                    state[4 * 3 + 0] = min(state[4 * 3 + 0], distance_y)
                elif distance_y < 0:
                    state[4 * 3 + 1] = min(state[4 * 3 + 1], -distance_y)

            if self.snake_head.y == body.y:
                distance_x = body.x - self.snake_head.x
                if distance_x > 0:
                    state[4 * 3 + 2] = min(state[4 * 3 + 2], distance_x)
                elif distance_x < 0:
                    state[4 * 3 + 3] = min(state[4 * 3 + 3], -distance_x)
        state[16] = len(self.snake_body) + 1

        return state

    def max_action(self):
            top = -1001
            action = -1
            for i in range(4):
                tmp = copy.deepcopy(self)
                if i == 0:
                    _, score = tmp.up()
                    if score > top:
                        top = score
                        action = i
                elif i == 1:
                    _, score = tmp.down()
                    if score > top:
                        top = score
                        action = i
                elif i == 2:
                    _, score = tmp.right()
                    if score > top:
                        top = score
                        action = i
                elif i == 3:
                    _, score = tmp.left()
                    if score > top:
                        top = score
                        action = i
            return action

        # for apple in self.green_apple:
        #     if apple.x == self.snake_head.x:
        #         if apple.y > self.snake_head.y and 1 in move_list:
        #             return 1
        #         elif apple.y < self.snake_head.y and 0 in move_list:
        #             return 0
        #     if apple.y == self.snake_head.y:
        #         if apple.x > self.snake_head.x and 2 in move_list:
        #             return 2
        #         elif apple.x < self.snake_head.x and 3 in move_list:
        #             return 3
        # for i in range(100):
        #     if action in move_list:
        #         return action
        # return action