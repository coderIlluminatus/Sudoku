DIMENSION = 9

class SudokuSolver(object):
    def __init__(self, board):
        self.initial_board = board
        self.board = self.initial_board

    def display_solution(self):
        output_file = open("solution.txt", "a")
        output_file.writelines(' '.join(str(element) for element in row) + '\n' for row in self.board)

    def get_first_blank(self):
        for row_number, row in enumerate(self.board):
            if 0 in row:
                return row_number, row.index(0)

    def get_one_box(self, i):
        return self.board[i : i+3] + self.board[i+9 : i+12] + self.board[i+18 : i+21]

    def get_all_boxes(self):
        return [self.get_one_box(i) for i in range(0, 61, 3)]

    def split_up(self):
        return [self.board[i * DIMENSION : (i + 1) * DIMENSION] for i in range(DIMENSION)]

    def check_consistency(self):
        return sum(DIMENSION - len(set(row)) for row in self.board)

    def check_constraints(self, row, column, number):
        if number in self.board[row]:
            return False
        if number in [self.board[i][column] for i in range(9)]:
            return False
        box_start = ((row // 3) * 3) * 9 + ((column // 3) * 3)
        if number in self.get_one_box(box_start):
            return False
        return True

    def possible_moves(self, row, column):
        possibilities = []
        for number in range(1, 10):
            if self.check_constraints(row, column, number):
                possibilities.append(number)
        return possibilities

    def is_solved(self):
        for row in self.board:
            if 0 in row:
                return False
        return True

    @staticmethod
    def mismatch(vector_a, vector_b):
        return sum(1 if element_a != element_b else 0 for element_a, element_b in zip(vector_a, vector_b))
