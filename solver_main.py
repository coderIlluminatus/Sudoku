import fileinput
from copy import deepcopy
from solvers.solver_simple_search import SolverSimpleSearch
from solvers.solver_backtracking import SolverBacktracking
from solvers.solver_genetic import SolverGenetic

def read_input():
    board = []
    for row in fileinput.input('input.txt'):
        board.append(list(map(int, row.strip().split())))
    return board

def main():
    board = read_input()
    simple_search = SolverSimpleSearch(deepcopy(board))
    simple_search.solve()

    backtracking = SolverBacktracking(deepcopy(board))
    backtracking.solve()

    genetic = SolverGenetic(deepcopy(board))
    genetic.solve()

if __name__ == '__main__':
    main()