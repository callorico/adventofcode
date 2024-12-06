import sys
import re
from typing import List, Tuple


def load_data(input_path: str) -> List[str]:
    with open(input_path, 'rt') as f:
        grid = []
        for line in f:
            cleaned = line.strip()
            if cleaned:
                grid.append(cleaned)

    return grid


def found_target(grid: List[str], sequence: List[Tuple[int, int]], target: str) -> bool:
    assert len(sequence) == len(target)
    num_rows = len(grid)
    num_cols = len(grid[0])

    for coordinate, letter in zip(sequence, target):
        row, col = coordinate
        if row < 0 or row >= num_rows or col < 0 or col >= num_cols:
            return False

        if grid[row][col] != letter:
            return False

    return True

def main(input_path):
    grid = load_data(input_path)

    # Part 1
    matches = 0
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            # Generate 4 letter index sequence in every direction
            sequences = [
                [(r-delta, c) for delta in range(4)],
                [(r+delta, c) for delta in range(4)],
                [(r, c+delta) for delta in range(4)],
                [(r, c-delta) for delta in range(4)],
                [(r+delta, c+delta) for delta in range(4)],
                [(r-delta, c+delta) for delta in range(4)],
                [(r+delta, c-delta) for delta in range(4)],
                [(r-delta, c-delta) for delta in range(4)]
            ]

            for sequence in sequences:
                if found_target(grid, sequence, "XMAS"):
                    matches += 1

    print(matches)

    # Part 2
    matches = 0

    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == "A":
                sequences = [
                    [(r+delta, c+delta) for delta in range(-1, 2)],
                    [(r-delta, c+delta) for delta in range(-1, 2)],
                    [(r+delta, c-delta) for delta in range(-1, 2)],
                    [(r-delta, c-delta) for delta in range(-1, 2)],
                ]

                x_leg_matches = 0
                for sequence in sequences:
                    if found_target(grid, sequence, "MAS"):
                        x_leg_matches += 1

                if x_leg_matches == 2:
                    matches += 1


    print(matches)


if __name__ == '__main__':
    main(sys.argv[1])



