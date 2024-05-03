import numpy as np

BLACK_START_POSITIONS = np.array([
    [0, 0], [0, 1], [0, 2], [0, 3], [0, 4],
    [1, 0], [1, 1], [1, 2], [1, 3], [1, 4],
    [2, 0], [2, 1], [2, 2], [2, 3],
    [3, 0], [3, 1], [3, 2],
    [4, 0], [4, 1]
])

WHITE_START_POSITIONS = np.array([[15 - x, 15 - y] for x, y in BLACK_START_POSITIONS])

BLACK_BASE = (15, 15)
WHITE_BASE = (0, 0)

BLACK = "BLACK"
WHITE = "WHITE"

BACKGROUND = '#f0d9b5'
