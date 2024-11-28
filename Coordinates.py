import random
BOARD_SIZE = 10


class Coordinates:
    def __init__(self, x=-1, y=-1):
        self.x = x
        self.y = y

    def random(self, size):
        self.x = random.randint(0, size - 1)
        self.y = random.randint(0, size - 1)

    def __eq__(self, value):
        if self.x == value.x and self.y == value.y:
            return True
        return False

    def __lt__(self, value):
        if self.x > value.x:
            return True
        if self.x == value.x and self.y > value.y:
            return True
        return False

    def eq(self, x, y):
        if self.x == x and self.y == y:
            return True
        return False

    def __repr__(self):
        return f"x: {self.x} y: {self.y}"

    def __hash__(self):
        return hash((self.x, self.y))

    def getCoordinates(self):
        return self.x, self.y
