import fileinput
from copy import deepcopy
from time import time
from solvers.solver_simple_search import SolverSimpleSearch
from solvers.solver_backtracking import SolverBacktracking
from solvers.solver_genetic import SolverGenetic

def read_input():
    board = []
    for row in fileinput.input('puzzle.txt'):
        board.append(list(map(int, row.strip().split())))
    return board

def main():
    board = read_input()

    output_file = open('solution.txt', 'w')
    output_file.write('SOLVING USING SIMPLE SEARCH ALGORITHM:\n')
    output_file.close()
    simple_search = SolverSimpleSearch(deepcopy(board))
    start_time = time()
    solved = simple_search.solve()
    running_time = time() - start_time
    output_file = open('solution.txt', 'a')
    output_file.write('RUNNING TIME: ' + str(running_time) + 's\n')
    output_file.close()
    if not solved:
        print('COULD NOT SOLVE BY SIMPLE SEARCH')

    output_file = open('solution.txt', 'a')
    output_file.write('\n\nSOLVING USING BACKTRACKING ALGORITHM:\n')
    output_file.close()
    backtracking = SolverBacktracking(deepcopy(board))
    start_time = time()
    solved = backtracking.solve()
    running_time = time() - start_time
    output_file = open('solution.txt', 'a')
    output_file.write('RUNNING TIME: ' + str(running_time) + 's\n')
    output_file.close()
    if not solved:
        print('COULD NOT SOLVE BY BACKTRACKING')

    genetic = SolverGenetic(deepcopy(board), 0.7, 0.2, 10000)
    start_time = time()
    solved = genetic.solve()
    running_time = time() - start_time
    output_file = open('solution.txt', 'a')
    output_file.write('RUNNING TIME: ' + str(running_time) + 's\n')
    output_file.close()
    if not solved:
        print('COULD NOT SOLVE BY GENETIC ALGORITHM')

if __name__ == '__main__':
    main()
