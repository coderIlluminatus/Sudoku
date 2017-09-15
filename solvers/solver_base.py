DIMENSION = 9

class SudokuSolver(object):
    def __init__(self, board):
        self.initial_board = board
        self.board = self.initial_board

    def get_one_box(self, i):
        return self.board[i : i+3] + self.board[i+9 : i+12] + self.board[i+18 : i+21]

    def get_all_boxes(self):
        return [self.get_one_box(i) for i in range(0, 61, 3)]

    def split_up(self):
        return [self.board[i * DIMENSION : (i + 1) * DIMENSION] for i in range(DIMENSION)]

    def check_consistency(self):
        return sum(DIMENSION - len(set(row)) for row in self.board)

    @staticmethod
    def mismatch(vector_a, vector_b):
        return sum(1 if element_a != element_b else 0 for element_a, element_b in zip(vector_a, vector_b))
