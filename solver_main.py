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

    output_file = open('output.txt', 'w')
    output_file.write('SOLVING USING SIMPLE SEARCH ALGORITHM:\n')
    output_file.close()
    simple_search = SolverSimpleSearch(deepcopy(board))
    solved = simple_search.solve()
    if not solved:
        print('COULD NOT SOLVE BY SIMPLE SEARCH')

    output_file = open('output.txt', 'a')
    output_file.write('\n\nSOLVING USING BACKTRACKING ALGORITHM:\n')
    output_file.close()
    backtracking = SolverBacktracking(deepcopy(board))
    solved = backtracking.solve()
    if not solved:
        print('COULD NOT SOLVE BY BACKTRACKING')

    # genetic = SolverGenetic(deepcopy(board))
    # solved = genetic.solve()
    # if not solved:
    #     print('COULD NOT SOLVE BY GENETIC ALGORITHM')

if __name__ == '__main__':
    main()