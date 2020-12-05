import sys
import re
from collections import Counter

FORMAT = re.compile(
    r'(?P<min>\d+)-(?P<max>\d+) (?P<char>\w): (?P<password>\w+)'
)

def load_data(input_path):
    with open(input_path, 'r') as f:
        return [line.strip() for line in f]

def trees_hit(matrix, delta_x, delta_y):
    x = 0
    y = 0
    width = len(matrix[0])
    height = len(matrix)

    # print(width, height)

    trees = 0
    while y < height:
        print(matrix[y][x])
        if matrix[y][x] == '#':
            trees += 1

        x = (x + delta_x) % width
        y += delta_y
        # print(x, y)

    return trees

def main(input_path):
    matrix = load_data(input_path)
    for line in matrix:
        print(line)
    x = 0
    y = 0
    width = len(matrix[0])
    height = len(matrix)

    print(width, height)

    a = trees_hit(matrix, 1, 1)
    b = trees_hit(matrix, 3, 1)
    c = trees_hit(matrix, 5, 1)
    d = trees_hit(matrix, 7, 1)
    e = trees_hit(matrix, 1, 2)

    print(a * b * c * d * e)
    # while y < height:
    #     print(matrix[y][x])
    #     if matrix[y][x] == '#':
    #         trees += 1

    #     x = (x + 3) % width
    #     y += 1
    #     print(x, y)

    # print(trees)

if __name__ == '__main__':
    main(sys.argv[1])