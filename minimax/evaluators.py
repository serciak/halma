import random

from game.Board import Board
from game.constants import WHITE, BLACK_BASE, WHITE_BASE, BLACK


def random_evaluator(board: Board):
    return random.randint(-100, 100)


def distance_evaluator(board: Board):
    white_distance = sum(manhattan_distance(pawn, BLACK_BASE) for pawn in board.get_pawns(WHITE))
    black_distance = sum(manhattan_distance(pawn, WHITE_BASE) for pawn in board.get_pawns(BLACK))

    return white_distance - black_distance


def distance_evaluator_v2(board: Board):
    score = 2 * distance_evaluator(board)


def manhattan_distance(pawn, goal):
    return abs(pawn.x - goal[0]) + abs(pawn.y - goal[1])
