import sys
from itertools import chain
from typing import List, Set, Tuple, Dict


def load_data(input_path: str) -> List[List[int]]:
    grid = []
    with open(input_path, 'r') as f:
        for line in f:
            grid.append([int(c) for c in line.strip()])

    return grid

def next_grid(grid: List[List[int]], offset: int) -> List[List[int]]:
    def incr(val: int) -> int:
        next = val + offset
        if next > 9:
            next -= 9
        return next

    incremented_grid = []
    for row in grid:
        incremented_grid.append([incr(v) for v in row])

    return incremented_grid

def print_grid(grid: List[List[int]]):
    for row in grid:
        print(''.join(str(v) for v in row))

def part2(input_path: str):
    grid_part = load_data(input_path)
    num_rows = len(grid_part)

    grids = [next_grid(grid_part, offset) for offset in range(10)]
    grid: List[List[int]] = []
    offsets = [
        [0, 1, 2, 3, 4],
        [1, 2, 3, 4, 5],
        [2, 3, 4, 5, 6],
        [3, 4, 5, 6, 7],
        [4, 5, 6, 7, 8],
    ]

    for offset in offsets:
        for row_index in range(num_rows):
            row: List[int] = list(
                chain.from_iterable(grids[i][row_index] for i in offset)
            )
            grid.append(row)

    print(f'Num rows: {len(grid)}')
    print(f'Num cols: {len(grid[0])}')
    print_grid(grid)

    dest_row = len(grid) - 1
    dest_col = len(grid[0]) - 1

    frontiers: Dict[Tuple[int, int], int] = {}
    frontiers[(0, 0)] = 0

    min_risks: Dict[Tuple[int, int], int] = {}

    while frontiers:
        new_frontiers: Dict[Tuple[int, int], int] = {}
        for cell, risk in frontiers.items():
            row, col = cell

            adjacent_cells = (
                (row - 1, col),
                (row + 1, col),
                (row, col - 1),
                (row, col + 1)
            )

            for next_row, next_col in adjacent_cells:
                if next_row < 0 or next_row > dest_row or next_col < 0 or next_col > dest_col:
                    continue

                new_risk = risk + grid[next_row][next_col]
                best_risk_so_far = min_risks.get((next_row, next_col))
                if best_risk_so_far is None or new_risk < best_risk_so_far:
                    # print(f'Best path to {next_row},{next_col} has cost {new_risk}')
                    min_risks[(next_row, next_col)] = new_risk
                    new_frontiers[(next_row, next_col)] = new_risk

                # Otherwise, this path is inferior to a previous one, ignore it

        frontiers = new_frontiers
    best_risk = min_risks[(dest_row, dest_col)]
    print(f'Total risk: {best_risk}')


def part1(input_path: str):
    grid = load_data(input_path)

    dest_row = len(grid) - 1
    dest_col = len(grid[0]) - 1

    frontiers: Dict[Tuple[int, int], int] = {}
    frontiers[(0, 0)] = 0

    min_risks: Dict[Tuple[int, int], int] = {}

    while frontiers:
        new_frontiers: Dict[Tuple[int, int], int] = {}
        for cell, risk in frontiers.items():
            row, col = cell

            adjacent_cells = (
                (row - 1, col),
                (row + 1, col),
                (row, col - 1),
                (row, col + 1)
            )

            for next_row, next_col in adjacent_cells:
                if next_row < 0 or next_row > dest_row or next_col < 0 or next_col > dest_col:
                    continue

                new_risk = risk + grid[next_row][next_col]
                best_risk_so_far = min_risks.get((next_row, next_col))
                if best_risk_so_far is None or new_risk < best_risk_so_far:
                    # print(f'Best path to {next_row},{next_col} has cost {new_risk}')
                    min_risks[(next_row, next_col)] = new_risk
                    new_frontiers[(next_row, next_col)] = new_risk

                # Otherwise, this path is inferior to a previous one, ignore it

        frontiers = new_frontiers

    best_risk = min_risks[(dest_row, dest_col)]
    print(f'Total risk: {best_risk}')




if __name__ == '__main__':
    part2(sys.argv[1])
