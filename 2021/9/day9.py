import sys
from typing import List, Set, Tuple


def load_data(input_path: str) -> List[List[int]]:
    with open(input_path, 'r') as f:
        grid = []
        for line in f:
            cleaned = line.strip()
            if cleaned:
                grid.append([int(c) for c in cleaned])

        return grid


def is_low_point(grid: List[List[int]], row: int, col: int) -> bool:
    rows = len(grid)
    cols = len(grid[0])

    val = grid[row][col]
    neighbors = [
        (row + 1, col),
        (row - 1, col),
        (row, col + 1),
        (row, col - 1),
    ]


    for r, c in neighbors:
        if r < 0 or r >= rows or c < 0 or c >= cols:
            continue

        if grid[row][col] >= grid[r][c]:
            return False

    return True


def part1(input_path: str):
    grid = load_data(input_path)
    rows = len(grid)
    cols = len(grid[0])

    total = 0
    for r in range(rows):
        for c in range(cols):
            if is_low_point(grid, r, c):
                print(f'Found low point: {grid[r][c]}')
                total += 1 + grid[r][c]

    print(total)


def basin_size(grid: List[List[int]], basins: Set[Tuple[int, int]], row: int, col: int) -> int:
    assert(grid[row][col] != 9)

    rows = len(grid)
    cols = len(grid[0])

    neighbors = [
        (row + 1, col),
        (row - 1, col),
        (row, col + 1),
        (row, col - 1),
    ]

    sum = 1
    basins.add((row, col))

    for r, c in neighbors:
        if r < 0 or r >= rows or c < 0 or c >= cols:
            continue

        if grid[r][c] == 9:
            continue

        if (r, c) in basins:
            continue

        if grid[row][col] < grid[r][c]:
            sum += basin_size(grid, basins, r, c)

    return sum


def part2(input_path: str):
    grid = load_data(input_path)
    rows = len(grid)
    cols = len(grid[0])

    basins: Set[Tuple[int, int]] = set()
    basin_sizes = []
    for r in range(rows):
        for c in range(cols):
            if is_low_point(grid, r, c):
                print(f'Found low point: {grid[r][c]}')
                basin_sizes.append(basin_size(grid, basins, r, c))

    basin_sizes.sort(key=lambda k: -k)
    print(basin_sizes)

    total = basin_sizes[0] * basin_sizes[1] * basin_sizes[2]
    print(total)



if __name__ == '__main__':
    part2(sys.argv[1])