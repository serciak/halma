import random
from functools import lru_cache

import numpy as np

from game import Pawn
from game.Board import Board
from game.constants import WHITE, BLACK_BASE, WHITE_BASE, BLACK, BLACK_START_POSITIONS, WHITE_START_POSITIONS


@lru_cache()
def generate_distance_weights(size):
    weights = np.zeros((size, size), dtype=int)

    for y in range(size):
        for x in range(size):
            # if [x, y] in BLACK_START_POSITIONS.tolist():
            #     weights[x, y] = -15
            # elif [x, y] in WHITE_START_POSITIONS.tolist():
            #     weights[x, y] = 15
            # else:
            #     weights[x, y] = abs(x) + abs(y) - 15
            weights[x, y] = abs(x) + abs(y) - 15

    return -weights


def random_evaluator(board: Board):
    return random.random()


def weight_distance_evaluator(board: Board):
    weights = generate_distance_weights(16)
    white_pawns = board.get_pawns(WHITE)
    black_pawns = board.get_pawns(BLACK)

    white_distance = sum(weights[pawn.x, pawn.y] for pawn in white_pawns)
    black_distance = sum(weights[pawn.x, pawn.y] for pawn in black_pawns)

    return white_distance + black_distance


def distance_evaluator(board: Board, dist_fun):
    white_distance = sum(dist_fun(pawn, BLACK_BASE) for pawn in board.get_pawns(WHITE))
    black_distance = sum(dist_fun(pawn, WHITE_BASE) for pawn in board.get_pawns(BLACK))

    return black_distance - white_distance


def m_distance_evaluator(board: Board):
    return distance_evaluator(board, manhattan_distance)


def e_distance_evaluator(board: Board):
    return distance_evaluator(board, euclidean_distance)


def base_penalty_evaluator(board: Board):
    return weight_distance_evaluator(board) - 2 * base_penalty(board)


def middle_bonus_evaluator(board: Board):
    return 2 * weight_distance_evaluator(board) + middle_bonus(board) + opponent_base_bonus(board)


def opponent_base_bonus_evaluator(board: Board):
    return m_distance_evaluator(board) + 2 * opponent_base_bonus(board)


def group_bonus_evaluator(board: Board):
    return weight_distance_evaluator(board) + 2 * group_bonus(board) + opponent_base_bonus(board)


def mixed_evaluator(board: Board):
    return 1.5 * weight_distance_evaluator(board) + middle_bonus(board) + group_bonus(board) + 2 * opponent_base_bonus(board) - 2 * base_penalty(board)


def group_bonus(board: Board):
    white_groups = count_connected_groups(board, WHITE)
    black_groups = count_connected_groups(board, BLACK)

    e = len(WHITE_START_POSITIONS) / (len(white_groups) + 1) - len(BLACK_START_POSITIONS) / (len(black_groups) + 1)
    return e


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


def opponent_base_bonus(board: Board):
    white_pawns = board.get_pawns(WHITE)
    black_pawns = board.get_pawns(BLACK)

    white_bonus = sum(1 if pawn.position() in BLACK_START_POSITIONS.tolist() else 0 for pawn in white_pawns)
    black_bonus = sum(1 if pawn.position() in WHITE_START_POSITIONS.tolist() else 0 for pawn in black_pawns)

    return white_bonus - black_bonus


def count_connected_groups(board: Board, player_color):
    connected_groups = []
    visited = set()
    for pawn in board.get_pawns(player_color):
        if pawn not in visited:
            group = set()
            dfs(board, pawn, player_color, visited, group)
            connected_groups.append(group)
    return connected_groups


def dfs(board: Board, pawn, player_color, visited, group):
    visited.add(pawn)
    group.add(pawn)
    x, y = pawn.x, pawn.y
    for nx in [x - 1, x, x + 1]:
        for ny in [y - 1, y, y + 1]:
            if not board.is_valid_move(nx, ny):
                continue

            neighbor = board.get_pawn(nx, ny)
            if neighbor != 0 and neighbor.color == player_color and neighbor not in visited:
                dfs(board, neighbor, player_color, visited, group)


def euclidean_distance(pawn, goal):
    return ((pawn.x - goal[0]) ** 2 + (pawn.y - goal[1]) ** 2) ** 0.5


def manhattan_distance(pawn, goal):
    return abs(pawn.x - goal[0]) + abs(pawn.y - goal[1])
