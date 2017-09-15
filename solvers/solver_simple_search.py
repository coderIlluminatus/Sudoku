from solvers.solver_base import SudokuSolver

class SolverSimpleSearch(SudokuSolver):
    def __init__(self, board):
        super(SolverSimpleSearch, self).__init__(board)

    def get_empty_cells(self):
        for row in range(9):
            for column in range(9):
                if self.board[row][column] == 0:
                    yield [row, column]

    def solve(self):
        empty_cells = list(self.get_empty_cells())
        cell_index = 0
        while cell_index < len(empty_cells):    
            cell = empty_cells[cell_index]
            number = self.board[cell[0]][cell[1]]   
            if number < 9:
                number += 1
                if self.check_constraints(cell[0], cell[1], number):
                    cell_index += 1
                self.board[cell[0]][cell[1]] = number
            else:
                number = 0
                self.board[cell[0]][cell[1]] = 0
                cell_index -= 1
                if cell_index < 0:
                    return False
        self.display_solution()
        return True
