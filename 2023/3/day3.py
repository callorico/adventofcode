import sys
from collections import defaultdict
from typing import Tuple, Optional


def load_data(input_path: str) -> list[str]:
    with open(input_path, "r") as f:
        grid = [l.strip() for l in f.readlines()]

    return grid


def update_gear_adjacencies(grid: list[str], value: int, adjacent_to_gear: dict[Tuple, list[int]], start: Tuple, end: Tuple) -> bool:
    assert start[0] == end[0], "Numbers can only appear on the same row"
    assert start[1] <= end[1], "End digit col must be after the start"

    for r in range(start[0] - 1, start[0] + 2):
        for c in range(start[1] - 1, end[1] + 2):
            if r < 0 or r >= len(grid):
                # Above or below the grid
                continue

            if c < 0 or c >= len(grid[0]):
                # Left or right of the grid
                continue

            if c >= start[1] and c <= end[1] and r == start[0]:
                assert grid[r][c].isdigit()
                # This is one of the digits
                continue

            if grid[r][c] == "*":
                adjacent_to_gear[(r, c)].append(value)


def main(input_path):
    grid: list[str] = load_data(input_path)
    rows: int = len(grid)
    cols: int = len(grid[0])

    adjacent_to_gears: dict[Tuple, list[int]] = defaultdict(list)

    for r in range(rows):
        start_digit_col: Optional[int] = None
        end_digit_col: Optional[int] = None

        for c in range(cols): 
            if grid[r][c].isdigit():
                if start_digit_col is None:
                    start_digit_col = c
                end_digit_col = c
            else:
                # Check to see if we've reached the end of a digit string
                if start_digit_col is not None:
                    value = int(grid[r][start_digit_col:end_digit_col + 1])
                    # print(f"{r},{c}: Parsed value: {value}")
                    update_gear_adjacencies(grid, value, adjacent_to_gears, (r, start_digit_col), (r, end_digit_col))
                    start_digit_col = None
                    end_digit_col = None

        if start_digit_col is not None:
            value = int(grid[r][start_digit_col:end_digit_col + 1])
            update_gear_adjacencies(grid, value, adjacent_to_gears, (r, start_digit_col), (r, end_digit_col))

    sum = 0
    for parts in adjacent_to_gears.values():
        if len(parts) == 2:
            gear_ratio = parts[0] * parts[1]
            sum += gear_ratio

    print(sum)


if __name__ == "__main__":
    main(sys.argv[1])