import logging
from copy import deepcopy
from random import random, randint, shuffle
from math import sqrt
from statistics import pstdev

from solvers.solver_base import SudokuSolver

class SolverGenetic(SudokuSolver):
    def __init__(self, board, probability_recombination, probability_mutation, population_limit):
        logging.basicConfig(filename='eventlog.txt', level=logging.DEBUG)
        super(SolverGenetic, self).__init__(board)
        self.probability_recombination = probability_recombination
        self.probability_mutation = probability_mutation
        self.population_limit = population_limit
        self.dimension = len(self.board)
        self.box_dimension = int(sqrt(len(self.board)))
        self.population = None
        self.fixed_indexes = None

    @staticmethod
    def inverse(T):
        return 1 // T

    def flatten(self):
        self.initial_board = sum(self.initial_board, [])
        self.board = sum(self.board, [])

    def reshape(self, board):
        return [board[i * self.dimension : (i + 1) * (self.dimension)] for i in range(self.dimension)]

    def display_genetic_solution(self, board, generation_count):
        output_file = open('solution.txt', 'a')
        output_file.writelines(' '.join(str(element) for element in row) + '\n' for row in board)
        output_file.write('NUMBER OF GENERATIONS: ' + str(generation_count) + '\n')
        output_file.write('POPULATION LIMIT: ' + str(self.population_limit) + '\n')
        output_file.write('PROBABILITY OF RECOMBINATION: ' + str(self.probability_recombination) + '\n')
        output_file.write('PROBABILITY OF MUTATION: ' + str(self.probability_mutation) + '\n')
        output_file.close()

    def set_fixed_indexes(self):
        self.fixed_indexes = []
        for index in range(self.dimension * self.dimension):
            if self.initial_board[index] != 0:
                self.fixed_indexes.append(index)

    def get_rows(self, board):
        boxes_row_major = []
        box_row = []
        for r in range(self.box_dimension):
            for f in range(self.box_dimension):
                for s in range(self.box_dimension):
                    board_row_number = s + (r * self.box_dimension)
                    for i in range(self.box_dimension):
                        element_of_subgrid = f*self.box_dimension+i
                        flattened_board_index = board_row_number*self.dimension + element_of_subgrid
                        box_row.append(board[flattened_board_index])
                boxes_row_major.append(list(box_row))
                box_row.clear()
        return boxes_row_major

    def get_columns(self, board):
        boxes_column_major = []
        box_column = []
        for r in range(self.box_dimension):
            for c in range(self.box_dimension):
                for s in range(self.box_dimension):
                    board_column_number = (s * self.box_dimension) + r
                    for i in range(self.box_dimension):
                        element_of_subgrid = i*self.box_dimension + c
                        flattened_board_index = board_column_number*self.dimension + element_of_subgrid
                        box_column.append(board[flattened_board_index])
                boxes_column_major.append(list(box_column))
                box_column.clear()
        return boxes_column_major

    # GENETIC ALGORITHM FUNCTIONS
    def initialize(self):
        self.population = [None] * self.population_limit

        for i in range(self.population_limit):
            self.population[i] = [-1] * (self.dimension * self.dimension)

            for j in range(self.dimension):
                permutation = list(range(1, self.dimension + 1))
                shuffle(permutation)
                for k in range(self.dimension):
                    self.population[i][(j * self.dimension) + k] = permutation[k]

            for index in self.fixed_indexes:
                row_number = index // self.dimension
                row = self.population[i][self.dimension * row_number : self.dimension * (row_number + 1)]
                fixed_value = self.initial_board[index]
                correct_index = index
                current_index = row.index(fixed_value) + (row_number * self.dimension)

                self.population[i][current_index] = self.population[i][correct_index]
                self.population[i][correct_index] = fixed_value

    def adaptation(self, board):
        collisions = 0
        boxes_row_major = self.get_rows(board)
        boxes_column_major = self.get_columns(board)
        
        for box in boxes_row_major:
            counter = [0] * self.dimension
            for number in box:
                counter[number - 1] += 1
            collisions += sum(count - 1 for count in counter if count > 1)

        for box in boxes_column_major:
            counter = [0] * self.dimension
            for number in box:
                counter[number - 1] += 1
            collisions += sum(count - 1 for count in counter if count > 1)
        
        if collisions == 0:
            return -1
        inverse_of_collisions = float(1 / collisions)
        return inverse_of_collisions

    def selection(self, fitness, sum_fitness):
        selection_chance = [fitness[i]/sum_fitness for i in range(len(fitness))]

        random_list = sorted([random() for i in range(self.population_limit)])
        sum_fitness, random_index = 0, 0
        selected_parents = []

        for i in range(self.population_limit):
            sum_fitness += selection_chance[i]
            while random_index < self.population_limit and sum_fitness > random_list[random_index]:
                selected_parents.append(self.population[i])
                random_index += 1
        return selected_parents

    def recombination(self, parents):
        next_generation = []
        while len(parents) > 1:
            parent_1 = parents[0]
            del parents[0]
            
            random_parent_index = randint(0, len(parents) - 1)
            parent_2 = parents[random_parent_index]
            del parents[random_parent_index]

            recombination_preference = random()
            if recombination_preference <= self.probability_recombination:
                cut_point = randint(0, self.dimension - 2) * self.dimension

                piece_1, piece_2 = parent_1[cut_point : ], parent_2[cut_point : ]
                child_1, child_2 = parent_1[ : cut_point] + piece_2, parent_2[ : cut_point] + piece_1
            else:
                child_1, child_2 = parent_1, parent_2
            next_generation += [child_1, child_2]
        if parents != []:
            next_generation.append(parents[0])
        return next_generation

    def mutation(self, next_generation):
        mutants = next_generation
        for i in range(self.population_limit):
            for j in range(self.dimension):
                mutation_preference = random()
                if mutation_preference <= self.probability_mutation:
                    element_1, element_2 = randint(0, self.dimension - 1), randint(0, self.dimension - 1)
                    index_1, index_2 = j * self.dimension + element_1, j * self.dimension + element_2

                    while element_1 == element_2 or index_1 in self.fixed_indexes or index_2 in self.fixed_indexes:
                        element_1, element_2 = randint(0, self.dimension - 1), randint(0, self.dimension - 1)
                        index_1, index_2 = j * self.dimension + element_1, j * self.dimension + element_2
                    
                    if index_1 not in self.fixed_indexes and index_2 not in self.fixed_indexes:
                        mutants[i][index_1], mutants[i][index_2] = mutants[i][index_2], mutants[i][index_1]
        return mutants
    
    def evolution(self):
        generation_count, min_index = 0, 0
        fitness = [self.adaptation(self.population[i]) for i in range(self.population_limit)]
        sum_fitness = sum(fitness)

        inverse_list = list(map(self.inverse, fitness))
        deviation = pstdev(inverse_list)
        
        output_file = open('solution.txt', 'a')
        print("Generation: ", 0, ": best result = ", inverse_list[fitness.index(max(fitness))]," worst result = ",max(inverse_list)," standard deviation = ",deviation)
        
        while True:
            if -1 in fitness:
                self.display_genetic_solution(self.reshape(self.population[fitness.index(-1)]), generation_count)
                exit()

            parents = self.selection(fitness, sum_fitness)
            next_generation = self.recombination(parents)
            self.population = self.mutation(next_generation)

            generation_count += 1

            fitness = [self.adaptation(self.population[i]) for i in range(self.population_limit)]
            sum_fitness = sum(fitness)

            inverse_list = list(map(self.inverse, fitness))
            print("Generation: ", generation_count, ": best result = ", inverse_list[fitness.index(max(fitness))], " worst result = ", max(inverse_list)," standard deviation = ", pstdev(inverse_list))
    
    def solve(self):
        self.flatten()
        self.set_fixed_indexes()
        self.initialize()
        self.evolution()
