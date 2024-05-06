from game.constants import WHITE, BLACK


class Minimax:
    def __init__(self, evaluator, max_depth):
        self.evaluator = evaluator
        self.max_depth = max_depth
        self.visited_nodes = 0

    def minimax(self, board, player):
        return self.__minimax(board, self.max_depth, float('-inf'), float('inf'), player == WHITE)

    def __minimax(self, board, depth, alpha, beta, is_max):
        self.visited_nodes += 1

        if depth == 0 or board.winner() is not None:
            return self.evaluator(board), board

        if is_max:
            best_evaluation = float("-inf")
            best = None

            for move in board.get_player_moves(WHITE):
                evaluation, _ = self.__minimax(move, depth - 1, alpha, beta, False)

                if evaluation > best_evaluation:
                    best_evaluation = evaluation
                    best = move

                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break

            return best_evaluation, best
        else:
            best_evaluation = float("inf")
            best = None

            for move in board.get_player_moves(BLACK):
                evaluation, _ = self.__minimax(move, depth - 1, alpha, beta, True)
                if evaluation < best_evaluation:
                    best_evaluation = evaluation
                    best = move

                beta = min(beta, evaluation)
                if beta <= alpha:
                    break

            return best_evaluation, best

    def basic_minimax(self, board, player):
        self.visited_nodes = 0
        return self.__basic_minimax(board, self.max_depth, player == WHITE)

    def __basic_minimax(self, board, depth, is_max):
        self.visited_nodes += 1

        if depth == 0 or board.winner() is not None:
            return self.evaluator(board), board

        if is_max:
            best_evaluation = float("-inf")
            best = None

            for move in board.get_player_moves(WHITE):
                evaluation, _ = self.__basic_minimax(move, depth - 1, False)

                if evaluation > best_evaluation:
                    best_evaluation = evaluation
                    best = move

            return best_evaluation, best
        else:
            best_evaluation = float("inf")
            best = None

            for move in board.get_player_moves(BLACK):
                evaluation, _ = self.__basic_minimax(move, depth - 1, True)

                if evaluation < best_evaluation:
                    best_evaluation = evaluation
                    best = move

            return best_evaluation, best
