from game.constants import WHITE


class Pawn:
    def __init__(self, color, x, y):
        self.x = x
        self.y = y
        self.color = color

    def position(self):
        return [self.x, self.y]

    def __repr__(self):
        return "@" if self.color == WHITE else "#"
