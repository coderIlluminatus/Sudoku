from solvers.solver_base import SudokuSolver

class SolverGenetic(SudokuSolver):
    def __init__(self, board):
        super(SolverGenetic, self).__init__(board)

    def estimate_fitness(self):
        pass

    def solve(self):
        pass
