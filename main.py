import time

from gif_utils import generate_gif
from minimax.Minimax import Minimax
from minimax.evaluators import *

SAVE_PATH = r"C:\Users\PC\PycharmProjects\halma\gifs"


def run_ai_vs_ai():
    board = Board()

    mm1 = Minimax(adaptive_evaluator, 1)
    mm2 = Minimax(base_penalty_evaluator, 1)

    rounds = 0
    t_sum = 0
    board.draw(SAVE_PATH, rounds)
    while not board.winner() and not rounds >= 250:
        t = time.time()
        e1, board = mm1.minimax(board, WHITE)
        t_sum += time.time() - t
        e2, board = mm2.minimax(board, BLACK)

        rounds += 1
        print(rounds)
        print(t_sum / rounds)
        print(mm1.visited_nodes / rounds)
        if rounds % 1 == 0:
            board.draw()
    board.draw()
    generate_gif(SAVE_PATH, SAVE_PATH)
    print(t_sum / rounds)
    print(mm1.visited_nodes / rounds)


def run_ai_vs_human():
    board = Board()

    mm1 = Minimax(mixed_evaluator, 1)

    rounds = 0
    board.draw()
    while not board.winner():
        while True:
            try:
                src_y = int(input("Enter the x coordinate of the pawn you want to move (1-16): ")) - 1
                src_x = int(input("Enter the y coordinate of the pawn you want to move (1-16): ")) - 1
                dest_y = int(input("Enter the x coordinate of the destination square (1-16): ")) - 1
                dest_x = int(input("Enter the y coordinate of the destination square (1-16): ")) - 1
                if not (0 < src_x <= 16 and 0 < src_y <= 16 and 0 < dest_x <= 16 and 0 < dest_y <= 16):
                    print("Coordinates out of bounds. Please enter coordinates within the range 1-16.")
                    continue
                pawn = board.get_pawn(src_x, src_y)
                if pawn == 0:
                    print("No pawn found at the specified coordinates. Please try again.")
                    continue
                if pawn.color != BLACK:
                    print("You can only move black pawns. Please select a black pawn.")
                    continue
                moves = board.get_moves(pawn)
                if (dest_x, dest_y) not in moves:
                    print("Invalid move. Please select a valid destination square.")
                    continue
                board.move(pawn, dest_x, dest_y)
                break
            except ValueError:
                print("Invalid input. Please enter integers for coordinates.")
        e2, board = mm1.minimax(board, WHITE)

        rounds += 1
        print(rounds)

        board.draw()


run_ai_vs_ai()

