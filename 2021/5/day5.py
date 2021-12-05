import sys
from typing import Tuple, Dict, Iterable, List, Optional
from collections import defaultdict

SparseGrid = Dict[int, Dict[int, int]]
Line = Tuple[Tuple[int, int], Tuple[int, int]]

def parse_coordinates(coord: str) -> Tuple[int, int]:
    x, y = coord.split(',')
    return int(x), int(y)


def step(
    start: Tuple[int, int],
    end: Tuple[int, int]
) -> Optional[Tuple[int, int]]:
    row_delta = end[0] - start[0]
    col_delta = end[1] - start[1]

    if row_delta != 0 and col_delta != 0 and abs(row_delta) != abs(col_delta):
        # Not a horizontal, vertical, or 45 degree line
        return None

    row_step = 0
    if row_delta != 0:
        row_step = int(row_delta / abs(row_delta))

    col_step = 0
    if col_delta != 0:
        col_step = int(col_delta / abs(col_delta))

    return (row_step, col_step)

def load_data(input_path: str) -> List[Line]:
    lines = []
    with open(input_path, 'r') as f:
        for line in f:
            if not line:
                continue
            start, end = line.split(' -> ')
            start_coord = parse_coordinates(start)
            end_coord = parse_coordinates(end)
            lines.append((start_coord, end_coord))

    return lines


def overlaps(grid: SparseGrid) -> int:
    total_overlaps = 0
    for row in grid.values():
        total_overlaps += sum(1 for v in row.values() if v > 1)

    return total_overlaps

def main(input_path):
    lines = load_data(input_path)
    grid: SparseGrid = defaultdict(lambda: defaultdict(int))

    for start_coord, end_coord in lines:
        increment = step(start_coord, end_coord)
        if not increment:
            # print(f'Ignoring {start_coord}, {end_coord}')
            continue

        # print(f'start: {start_coord}, end: {end_coord}, step: {increment}')
        current = start_coord
        while True:
            row, col = current
            grid[row][col] += 1
            # print(f'Incremented {row} {col} to {grid[row][col]}')
            if current == end_coord:
                break
            current = (row + increment[0], col + increment[1])

    print(overlaps(grid))

if __name__ == '__main__':
    main(sys.argv[1])