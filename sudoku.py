#!/usr/bin/env python3

import argparse


def main():
    parser = argparse.ArgumentParser(description='Sudoku Solver')
    parser.add_argument('sudoku', nargs='?',
                        help="The sudoku to be solved. Known values are indicated with their numerical value from 1 to "
                             "9. Unknown values are indicated with either the numeral '0', an underscore, '_', or a "
                             "space. The values in the sudoku are ordered left to right, top to bottom. Each new row "
                             "begins every nine characters. A vertical pipe, '|', can optionally be placed between each"
                             " row to aid with readability, but is not necessary. If this argument is not supplied, an "
                             "interactive sudoku input tool will be used to supply the sudoku to be solved")
    args = parser.parse_args()


if __name__ == '__main__':
    main()