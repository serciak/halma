from copy import deepcopy
import random

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import FixedLocator

from game.Pawn import Pawn
from game.constants import *


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

    def move(self, pawn, x, y):
        self.board[x, y], self.board[pawn.x, pawn.y] = self.board[pawn.x, pawn.y], self.board[x, y]
        pawn.x, pawn.y = x, y

    def get_pawn(self, x, y):
        return self.board[x, y]

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

    def get_player_moves(self, color):
        moves = []

        for pawn in self.get_pawns(color):
            for x, y in self.get_moves(pawn):
                new_board = deepcopy(self)
                temp_pawn = new_board.get_pawn(pawn.x, pawn.y)

                new_board.move(temp_pawn, x, y)

                moves.append(new_board)
        random.shuffle(moves)
        return moves

    def get_jumps(self, pawn, start_x, start_y, visited):
        jumps = []

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue

                x = start_x + dx
                y = start_y + dy

                if self.is_valid_move(x, y) and self.board[x, y] != 0:
                    x_next = x + dx
                    y_next = y + dy

                    if self.is_valid_move(x_next, y_next) and self.board[x_next, y_next] == 0 and (
                            x_next, y_next) not in visited:
                        jumps.append((x_next, y_next))
                        visited.append((x_next, y_next))

                        jumps.extend(self.get_jumps(pawn, x_next, y_next, visited))

        return jumps

    def winner(self):
        white_pawns = self.get_pawns(WHITE)
        black_pawns = self.get_pawns(BLACK)

        white_wins = all(pawn.position() in BLACK_START_POSITIONS.tolist() for pawn in white_pawns)
        black_wins = all(pawn.position() in WHITE_START_POSITIONS.tolist() for pawn in black_pawns)

        if white_wins:
            return WHITE
        if black_wins:
            return BLACK
        return None

    def draw(self):
        fig, ax = plt.subplots()

        ax.set_xticks(np.arange(-0.5, 16, 1), minor=True)
        ax.set_yticks(np.arange(-0.5, 16, 1), minor=True)
        ax.grid(which='minor', color='black', linestyle='-', linewidth=1)
        ax.set_aspect(1)
        ax.set_facecolor(BACKGROUND)

        for x, y in BLACK_START_POSITIONS:
            ax.scatter(x, y, s=10, facecolors="black")
            ax.scatter(15 - x, 15 - y, s=10, facecolors="darkgrey")

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
