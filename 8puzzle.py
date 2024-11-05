import copy
import math
import timeit
import sys

import numpy as np

final_state = [[1, 2, 3],
               [4, 5, 6],
               [7, 8, 0]]
initial_state = [[1, 2, 3],
                 [4, 5, 6],
                 [0, 8, 7]]

len_row = len(final_state[0])  # number of items in each row
len_column = len(final_state)  # number of items in each column
space = []  # location of zero
open_set = [initial_state]
all_h = []
close_set = [initial_state]


def calculate_h(matrix):  # my heuristic
    h = 0
    if matrix is None:
        return math.inf
    for i in range(len_row):
        for j in range(len_column):
            exist_row = False
            exist_column = False
            if final_state[i][j] == 0:
                continue  # don't use 0 in calculating h
            for d in range(len_column):  # search in column
                if final_state[i][j] == matrix[i][d]:
                    exist_row = True
            if not exist_row:
                h = h + 1
            for k in range(len_row):  # search in row
                if final_state[i][j] == matrix[k][j]:
                    exist_column = True
            if not exist_column:
                h = h + 1
    return h


def find_location(number, matrix):
    return [[index, row.index(number)] for index, row in enumerate(matrix) if number in row][0]


def inversions(s):
    flat_list = []
    for sublist in s:
        for item in sublist:
            flat_list.append(item)
    flat_list = np.array(flat_list)
    k = flat_list[flat_list != 0]
    tinv = 0
    for i in range(len(k) - 1):
        b = np.array(np.where(k[i + 1:] < k[i])).reshape(-1)
        tinv += len(b)
    return tinv


def check(matrix):
    for d in range(len(close_set)):
        same_matrix = True
        for i in range(len_row):
            for j in range(len_column):
                if close_set[d][i][j] != matrix[i][j]:
                    same_matrix = False
        if same_matrix:
            return False
    close_set.append(matrix)
    return True


def move_up():
    if space[0] == 0:
        return None  # cant move up
    row = space[0]  # row of zero
    column = space[1]  # column of zero
    new_matrix = copy.deepcopy(initial_state)
    new_matrix[row - 1][column] = initial_state[row][column]  # swap with zero
    new_matrix[row][column] = initial_state[row - 1][column]  # swap with zero
    return new_matrix


def move_down():
    if space[0] == len_column - 1:
        return None  # cant move down
    row = space[0]  # row_of_zero
    column = space[1]  # column_of_zero
    new_matrix = copy.deepcopy(initial_state)
    new_matrix[row + 1][column] = initial_state[row][column]  # swap with zero
    new_matrix[row][column] = initial_state[row + 1][column]  # swap with zero
    return new_matrix


def move_right():
    if space[1] == len_row - 1:
        return None  # cant move right
    row = space[0]  # row_of_zero
    column = space[1]  # column_of_zero
    new_matrix = copy.deepcopy(initial_state)
    new_matrix[row][column + 1] = initial_state[row][column]  # swap with zero
    new_matrix[row][column] = initial_state[row][column + 1]  # swap with zero
    return new_matrix


def move_lef():
    if space[1] == 0:
        return None  # cant move left
    row = space[0]  # row_of_zero
    column = space[1]  # column_of_zero
    new_matrix = copy.deepcopy(initial_state)
    new_matrix[row][column - 1] = initial_state[row][column]  # swap with zero
    new_matrix[row][column] = initial_state[row][column - 1]  # swap with zero
    return new_matrix


if __name__ == '__main__':
    # Count inversions in given 8 puzzle
    invCount = inversions(initial_state)
    # return true if inversion count is even.
    if invCount % 2 != 0:
        print('Not Solvable')
        sys.exit()
    print_format = '{:' + str(len_row) + '}'
    start = timeit.default_timer()
    all_h.append(calculate_h(initial_state))
    step = 0
    number_of_nodes = 1
    while len(open_set) > 0:
        step = step + 1
        min_h_index = all_h.index(min(all_h))
        initial_state = open_set.pop(min_h_index)
        current_h = all_h.pop(min_h_index)
        print('\n'.join([''.join([print_format.format(item) for item in row])
                         for row in initial_state]))
        print()
        if current_h == 0:
            break
        space = find_location(0, initial_state)
        move = [move_right(), move_down(), move_lef(), move_up()]
        for matrix in move:
            if matrix is not None and check(matrix):
                open_set.append(matrix)
                all_h.append(calculate_h(matrix))
                number_of_nodes = number_of_nodes + 1
    stop = timeit.default_timer()
    print("number of nodes: " + str(number_of_nodes))
    print("step: " + str(step))
    print('Time: ', stop - start)
