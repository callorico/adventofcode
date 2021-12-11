import sys
from typing import List, Set, Tuple

def load_data(input_path: str) -> List[List[int]]:
    grid = []
    with open(input_path, 'r') as f:
        for line in f:
            grid.append([int(c) for c in line.strip()])
    return grid


def apply_flash(
    grid: List[List[int]],
    flashed: Set[Tuple[int, int]],
    row: int,
    col: int
) -> int:
    if grid[row][col] <= 9:
        return

    if (row, col) in flashed:
        return

    flashed.add((row, col))

    rows = len(grid)
    cols = len(grid[0])

    for r_delta in [-1, 0, 1]:
        for c_delta in [-1, 0, 1]:
            neighbor_row = row + r_delta
            neighbor_col = col + c_delta
            if neighbor_row < 0 or neighbor_row >= rows or neighbor_col < 0 or neighbor_col >= cols:
                continue

            grid[neighbor_row][neighbor_col] += 1
            apply_flash(grid, flashed, neighbor_row, neighbor_col)


def print_grid(grid: List[List[int]]):
    for row in grid:
        print(''.join(str(v) for v in row))

def part2(input_path: str):
    grid = load_data(input_path)
    print_grid(grid)

    rows = len(grid)
    cols = len(grid[0])
    for step in range(2000):
        # Increment each cell by 1
        next = []
        for row in grid:
            next.append([val + 1 for val in row])

        flashed = set()
        for r in range(rows):
            for c in range(cols):
                apply_flash(next, flashed, r, c)

        if len(flashed) == rows * cols:
            print(f'All flashed on step {step + 1}')
            return

        # print(f'Flashed: {flashed}')
        for r, c in flashed:
            next[r][c] = 0

        grid = next
        # print(f'Iteration {step+1}')
        # print_grid(grid)


def part1(input_path: str):
    grid = load_data(input_path)
    print_grid(grid)

    flashes = 0
    rows = len(grid)
    cols = len(grid[0])
    for step in range(100):
        # Increment each cell by 1
        next = []
        for row in grid:
            next.append([val + 1 for val in row])

        flashed = set()
        for r in range(rows):
            for c in range(cols):
                apply_flash(next, flashed, r, c)

        flashes += len(flashed)
        # print(f'Flashed: {flashed}')
        for r, c in flashed:
            next[r][c] = 0

        grid = next
        # print(f'Iteration {step+1}')
        # print_grid(grid)

    print(f'Flashes: {flashes}')

if __name__ == '__main__':
    part2(sys.argv[1])