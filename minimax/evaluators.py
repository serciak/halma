import random
from functools import lru_cache

import numpy as np

from game.Board import Board
from game.constants import WHITE, BLACK_BASE, WHITE_BASE, BLACK, BLACK_START_POSITIONS, WHITE_START_POSITIONS


def random_evaluator(board: Board):
    return random.randint(-100, 100)


def distance_evaluator(board: Board, dist_fun):
    white_distance = sum(dist_fun(pawn, BLACK_BASE) for pawn in board.get_pawns(WHITE))
    black_distance = sum(dist_fun(pawn, WHITE_BASE) for pawn in board.get_pawns(BLACK))

    return white_distance - black_distance


def m_distance_evaluator(board: Board):
    return distance_evaluator(board, manhattan_distance)


def e_distance_evaluator(board: Board):
    return distance_evaluator(board, euclidean_distance)


def base_penalty_evaluator(board: Board):
    return m_distance_evaluator(board) - base_penalty(board)


def middle_bonus_evaluator(board: Board):
    return m_distance_evaluator(board) + middle_bonus(board)


def base_penalty(board: Board):
    white_pawns = board.get_pawns(WHITE)
    black_pawns = board.get_pawns(BLACK)

    white_penalty = sum(1 if pawn.position() in WHITE_START_POSITIONS.tolist() else 0 for pawn in white_pawns)
    black_penalty = sum(1 if pawn.position() in BLACK_START_POSITIONS.tolist() else 0 for pawn in black_pawns)

    return white_penalty - black_penalty


def middle_bonus(board: Board):
    @lru_cache
    def generate_middle_bonus_weights(size):
        weights = np.zeros((size, size), dtype=int)

        for y in range(size):
            for x in range(size):
                distance_to_diagonal = abs(x - y)
                bonus_weight = size - distance_to_diagonal
                weights[y, x] = 16 if bonus_weight > 13 else bonus_weight

        return weights

    weights = generate_middle_bonus_weights(16)
    white_pawns = board.get_pawns(WHITE)
    black_pawns = board.get_pawns(BLACK)

    white_bonus = sum(weights[pawn.x, pawn.y] for pawn in white_pawns)
    black_bonus = sum(weights[pawn.x, pawn.y] for pawn in black_pawns)

    return white_bonus - black_bonus


def euclidean_distance(pawn, goal):
    return ((pawn.x - goal[0]) ** 2 + (pawn.y - goal[1]) ** 2) ** 0.5


def manhattan_distance(pawn, goal):
    return abs(pawn.x - goal[0]) + abs(pawn.y - goal[1])
