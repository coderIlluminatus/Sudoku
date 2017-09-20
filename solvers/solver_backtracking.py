from copy import deepcopy
from solvers.solver_base import SudokuSolver

class SolverBacktracking(SudokuSolver):
    def __init__(self, board):
        super(SolverBacktracking, self).__init__(board)

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
