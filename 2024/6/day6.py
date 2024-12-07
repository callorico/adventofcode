import sys
import re
from typing import List, Tuple, Dict, Set
from itertools import cycle


def load_data(input_path: str) -> Tuple[Tuple[int, int], List[str]]:
    grid = []
    guard_row = -1
    guard_col = -1

    with open(input_path, 'rt') as f:
        for line in f:
            cleaned = line.strip()
            if cleaned:
                if guard_col == -1:
                    try:
                        guard_col = cleaned.index("^")
                    except ValueError:
                        pass
                    else:
                        guard_row = len(grid)
                grid.append(cleaned)


    assert guard_row != -1 and guard_col != -1
    return (guard_row, guard_col), grid


def in_bounds(guard_position: Tuple[int, int], grid: List[str]) -> bool:
    row, col = guard_position
    return row >= 0 and row < len(grid) and col >= 0 and col < len(grid[0])


def is_blocked(guard_position: Tuple[int, int], grid: List[str]) -> bool:
    if not in_bounds(guard_position, grid):
        return False

    return grid[guard_position[0]][guard_position[1]] == "#"


def main(input_path):
    guard_position, grid = load_data(input_path)
    rotations = cycle([
        # Up
        (-1, 0),
        # Right
        (0, 1),
        # Down
        (1, 0),
        # Left
        (0, -1)
    ])
    visited_positions = set()
    direction = next(rotations)

    while True:
        visited_positions.add(guard_position)
        while True:
            proposed_next_position = (guard_position[0] + direction[0], guard_position[1] + direction[1])
            if is_blocked(proposed_next_position, grid):
                direction = next(rotations)
            else:
                break

        if not in_bounds(proposed_next_position, grid):
            break
        guard_position = proposed_next_position

    print(len(visited_positions))


if __name__ == '__main__':
    main(sys.argv[1])
