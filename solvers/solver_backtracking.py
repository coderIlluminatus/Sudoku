from copy import deepcopy
from solvers.solver_base import SudokuSolver

class SolverBacktracking(SudokuSolver):
    def __init__(self, board):
        super(SolverBacktracking, self).__init__(board)

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

    def solve(self):
        if self.is_solved():
            self.display_solution()
            return True

        blank_row_index, blank_column_index = self.get_first_blank()
        possibilities = self.possible_moves(blank_row_index, blank_column_index)

        if possibilities != []:
            for number in possibilities:
                new_state = deepcopy(self)
                new_state.board[blank_row_index][blank_column_index] = number
                is_solved = new_state.solve()
                if is_solved == True:
                    return True
        return False
