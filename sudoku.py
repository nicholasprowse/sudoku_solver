#!/usr/bin/env python3

import argparse
import numpy as np
import sys

# S indicates single lines and D indicates double lines
# For the cross characters, the weight of the horizontal line comes first
BOX_CHARS = {"HOR S": '\u2500', "HOR D": '\u2550', "VER S": '\u2502', "VER D": '\u2551', "TOP LEFT": '\u2554',
             "TOP RIGHT": '\u2557', "BOTTOM LEFT": '\u255A', "BOTTOM RIGHT": '\u255D', "TOP D": '\u2566',
             "TOP S": '\u2564', "LEFT D": '\u2560', "LEFT S": '\u255F', "RIGHT D": '\u2563', "RIGHT S": '\u2562',
             "CROSS SS": '\u253C', "CROSS DD": '\u256C', "CROSS SD": '\u256B', "CROSS DS": '\u256A',
             "BOTTOM S": '\u2567', "BOTTOM D": '\u2569'}


def print_sudoku(sudoku):
    """
    Prints the given sudoku to the screen. Box drawing characters are used to make this look nice. The 3x3 blocks in a
    sudoku are also represented by double lines
    :param sudoku: 9x9 numpy array of a sudoku
    """
    print(BOX_CHARS['TOP LEFT'], end="")
    for x in range(8):
        w = 'D' if x % 3 == 2 else 'S'
        print(3 * BOX_CHARS['HOR D'] + BOX_CHARS[f'TOP {w}'], end="")
    print(3 * BOX_CHARS['HOR D'] + BOX_CHARS['TOP RIGHT'])

    for y in range(9):
        print(BOX_CHARS['VER D'], end="")
        chars = [str(i) if i != 0 else " " for i in sudoku[:, y]]
        for x in range(8):
            w = 'D' if x % 3 == 2 else 'S'
            print(f" {chars[x]} {BOX_CHARS[f'VER {w}']}", end="")
        print(f" {chars[-1]} {BOX_CHARS['VER D']}")
        if y == 8:
            break

        hw = 'D' if y % 3 == 2 else 'S'
        print(BOX_CHARS[f'LEFT {hw}'], end="")
        for x in range(8):
            print(3 * BOX_CHARS[f'HOR {hw}'], end="")
            vw = 'D' if x % 3 == 2 else 'S'
            print(BOX_CHARS[f'CROSS {hw}{vw}'], end="")
        print(3 * BOX_CHARS[f'HOR {hw}'], end="")
        print(BOX_CHARS[f'RIGHT {hw}'])

    print(BOX_CHARS['BOTTOM LEFT'], end="")
    for x in range(8):
        w = 'D' if x % 3 == 2 else 'S'
        print(3 * BOX_CHARS['HOR D'] + BOX_CHARS[f'BOTTOM {w}'], end="")
    print(3 * BOX_CHARS['HOR D'] + BOX_CHARS['BOTTOM RIGHT'])


def error(message):
    """Prints the given message to standard error and exits execution"""
    sys.stderr.write(message + '\n')
    raise SystemExit


def parse_input(args):
    """
    Parses the input arguments into a 9x9 numpy array representing the sudoku. Input args is an array of strings.
    Each string is a comma separated string of rows. Each row must be exactly 9 characters, and there must be exactly
    9 rows across the list of strings. If these conditions aren't met, an error is displayed to the user. Numerical
    values are directly converted to ints, while underscores are converted to zeros (indicating the absence of a value)

    :param args: list of comma separated rows
    :return: 9x9 numpy array representing the sudoku, where absent values are represented by 0
    """
    args = [i.split(",") for i in args]
    num_rows = sum([len(i) for i in args])
    if num_rows != 9:
        error(f"Input Error: Sudoku must contain 9 rows, but {num_rows} have been given")
    sudoku = np.uint8(np.zeros((9, 9)))
    row = 0
    for i in args:
        for j in i:
            if len(j) != 9:
                error(f"Input Error: Every row must have 9 characters, but row {row + 1} has {len(j)} characters")
            for col in range(9):
                c = j[col]
                if c == '_':
                    c = '0'
                try:
                    sudoku[col, row] = int(c)
                except ValueError:
                    error(f"Input Error: The character '{c}' on row {row+1}, column {col+1} is invalid. Only the "
                          f"numeric digits, 0 to 9, and underscores are allowed")
            row += 1

    return sudoku


def brute_force_solve(sudoku):
    """
    Brute force approach to solving the sudoku. This works by finding the first unknown value, and checking the row,
    column and box to determine which values can go there. Each value is then tried, and the function is recursively
    called with the new sudoku. This can solve easy sudoku's, but is very slow for harder sudoku's
    :param sudoku: 3x3 numpy array containing the sudoku to be solved
    :return: 3x3 numpy array containing the solved sudoku
    """
    for y in range(9):
        for x in range(9):
            if sudoku[x, y] == 0:
                potential_values = [True] * 9

                for i in range(9):
                    # Check row
                    if sudoku[i, y] != 0:
                        potential_values[sudoku[i, y]-1] = False
                    # Check col
                    if sudoku[x, i] != 0:
                        potential_values[sudoku[x, i]-1] = False
                    # Check box
                    val = sudoku[3 * (x // 3) + i // 3, 3 * (y // 3) + i % 3]
                    if val != 0:
                        potential_values[val-1] = False

                for i in range(9):
                    if potential_values[i]:
                        sudoku[x, y] = i + 1
                        solution = brute_force_solve(sudoku)
                        if solution is not None:
                            return solution
                        sudoku[x, y] = 0

                return None
    # If you get to the end, there are no zeros, so it's already solved
    return sudoku


def get_sudoku_from_interactive_input():
    return 'Interactive Input'


def main():
    parser = argparse.ArgumentParser(description='Sudoku Solver')
    parser.add_argument('sudoku', nargs='*',
                        help="The sudoku to be solved. Known values are indicated with their numerical value from 1 to "
                             "9. Unknown values are indicated with either the numeral '0' or an underscore, '_'. The "
                             "values in the sudoku are ordered left to right, top to bottom. Each new row begins every "
                             "nine characters. Each row is separated with either a space or a comma. If this argument "
                             "is not supplied, an interactive sudoku input tool will be used to supply the sudoku to "
                             "be solved")

    args = parser.parse_args()
    if args.sudoku is None:
        sudoku = get_sudoku_from_interactive_input()
    else:
        sudoku = parse_input(args.sudoku)

    print_sudoku(sudoku)
    solution = brute_force_solve(sudoku)
    if solution is None:
        print('This sudoku has no solutions')
    else:
        print_sudoku(solution)


if __name__ == '__main__':
    main()
