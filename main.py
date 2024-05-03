import time

from game.Board import Board
from game.constants import WHITE, BLACK, BLACK_START_POSITIONS
from minimax.Minimax import Minimax
from minimax.evaluators import *

board = Board()

minimax1 = Minimax(middle_bonus_evaluator, 1)
minimax2 = Minimax(base_penalty_evaluator, 1)

for x in range(1000):
    print(x)
    e, board = minimax1.minimax(board, WHITE)

    if x % 10 == 0:
        board.draw()
    if board.winner():
        board.draw()
        print(board.winner())
        print(board.board)
        break

    e, board = minimax2.minimax(board, BLACK)
    if board.winner():
        board.draw()
        print(board.winner())
        print(board.board)
        break