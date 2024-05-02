import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import FixedLocator

from Pawn import Pawn
from constants import *


class Board:
    def __init__(self):
        self.board = None
        self.create_board()

    def create_board(self):
        self.board = np.zeros((16, 16), dtype=object)

        for x, y in BLACK_START_POSITIONS:
            self.board[x, y] = Pawn(BLACK, x, y)

        for x, y in WHITE_START_POSITIONS:
            self.board[x, y] = Pawn(WHITE, x, y)

    def is_valid_move(self, x, y):
        if x < 0 or x >= 16 or y < 0 or y >= 16:
            return False

        return True

    def get_pawns(self, color):
        return [pawn for row in self.board for pawn in row if pawn != 0 and pawn.color == color]

    def get_moves(self, pawn):
        moves = []

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue  # skip this position

                x = pawn.x + dx
                y = pawn.y + dy

                if self.is_valid_move(x, y):
                    square = self.board[x, y]

                    if square == 0:
                        moves.append((x, y))
                        continue

                    if square != 0:
                        x, y = x + dx, y + dy

                        if self.is_valid_move(x, y) and self.board[x, y] == 0:
                            moves.append((x, y))
                            visited = [(pawn.x, pawn.y)]

                            jumps = self.get_jumps(pawn, x, y, visited)
                            if jumps:
                                moves += jumps

        return moves

    def get_jumps(self, pawn, x, y, visited):
        jumps = []

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue

                x = x + dx
                y = y + dy

                if self.is_valid_move(x, y) and self.board[x, y] != 0:
                    x, y = x + dx, y + dy

                    if self.is_valid_move(x, y) and self.board[x, y] == 0 and (x, y) not in visited:
                        jumps.append((x, y))
                        visited.append((x, y))

                        jumps.extend(self.get_jumps(pawn, x, y, visited))

        return jumps

    def draw(self):
        fig, ax = plt.subplots()

        ax.set_xticks(np.arange(-0.5, 16, 1), minor=True)
        ax.set_yticks(np.arange(-0.5, 16, 1), minor=True)
        ax.grid(which='minor', color='black', linestyle='-', linewidth=1)
        ax.set_aspect(1)
        ax.set_facecolor(BACKGROUND)

        for y in range(16):
            for x in range(16):
                pawn = self.board[y, x]
                if isinstance(pawn, Pawn):
                    color = 'black' if pawn.color == BLACK else 'lightgrey'
                    ax.scatter(x, y, s=170, facecolors=color, edgecolors="black")

        ax.xaxis.set_ticks_position('none')
        ax.yaxis.set_ticks_position('none')

        ax.xaxis.set_major_locator(FixedLocator(np.arange(0, 16)))
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: int(x + 1)))
        ax.yaxis.set_major_locator(FixedLocator(np.arange(0, 16)))
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: int(y + 1)))

        plt.show()
