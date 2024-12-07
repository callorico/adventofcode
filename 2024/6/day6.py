import sys
import re
from typing import List, Tuple, Dict, Set, Iterable
from itertools import cycle
from collections import defaultdict


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


def run_guard(guard_position: Tuple[int, int], grid: List[str]) -> Tuple[bool, Iterable[Tuple[int, int]]]:
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

    visited_positions: Dict[Tuple[int, int], Tuple[int, int]] = defaultdict(set)
    direction = next(rotations)

    while True:
        if direction in visited_positions[guard_position]:
            # Cycle detected
            return True, visited_positions.keys()
        else:
            visited_positions[guard_position].add(direction)

        while True:
            proposed_next_position = (guard_position[0] + direction[0], guard_position[1] + direction[1])
            if is_blocked(proposed_next_position, grid):
                direction = next(rotations)
            else:
                break

        if not in_bounds(proposed_next_position, grid):
            break
        guard_position = proposed_next_position

    return False, visited_positions.keys()


def generate_new_grid(source_grid: List[str], row: int, col: int, new_value: str) -> List[str]:
    assert row >= 0 and row < len(source_grid)
    assert col >= 0 and col < len(source_grid[0])
    assert len(new_value) == 1

    row_to_modify = source_grid[row]
    modified_row = row_to_modify[:col] + new_value + row_to_modify[col+1:]
    copy = source_grid[:row] + [modified_row] + source_grid[row+1:]

    return copy

def main(input_path):
    guard_position, grid = load_data(input_path)

    # Part 1
    _, visited = run_guard(guard_position, grid)
    print(len(visited))

    # Part 2
    candidates = set(visited)
    for r, c in visited:
        candidates.add((r + 1, c))
        candidates.add((r - 1, c))
        candidates.add((r, c + 1))
        candidates.add((r, c - 1))

    loop_positions = 0
    for r, c in candidates:
        if in_bounds((r, c), grid) and grid[r][c] == ".":
            # Create a proposed grid with an obstacle at this position
            proposed_grid = generate_new_grid(grid, r, c, "#")
            cycle, _ = run_guard(guard_position, proposed_grid)
            if cycle:
                loop_positions += 1

    print(loop_positions)



if __name__ == '__main__':
    main(sys.argv[1])
