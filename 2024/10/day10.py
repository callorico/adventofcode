import sys
from typing import List, Tuple, Optional, Set


def load_data(input_path: str) -> List[List[int]]:
    grid = []
    with open(input_path, 'rt') as f:
        for line in f:
            grid.append([int(c) for c in line.strip()])

    return grid


def move(grid: List[List[int]], visited: Set[Tuple[int, int]], position: Tuple[int, int], delta: Tuple[int, int]) -> Optional[Tuple[int, int]]:
    value = grid[position[0]][position[1]]

    new_pos_row = position[0] + delta[0]
    new_pos_col = position[1] + delta[1]

    if new_pos_row < 0 or new_pos_row >= len(grid):
        return None

    if new_pos_col < 0 or new_pos_col >= len(grid[0]):
        return None

    new_value = grid[new_pos_row][new_pos_col]
    if new_value != value + 1:
        return None

    new_pos = (new_pos_row, new_pos_col)
    if new_pos in visited:
        return None

    return new_pos


def count_paths(grid: List[List[int]], trailhead: Tuple[int, int]) -> int:
    frontier = [trailhead]
    visited: Tuple[int, int] = set(frontier)
    reached_end = 0
    while frontier:
        head = frontier.pop()
        for delta in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            next_pos = move(grid, visited, head, delta)
            if next_pos:
                visited.add(next_pos)
                if grid[next_pos[0]][next_pos[1]] == 9:
                    reached_end += 1
                else:
                    frontier.append(next_pos)

    return reached_end


def main(input_path):
    grid = load_data(input_path)

    trailheads: List[Tuple[int, int]] = []
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == 0:
                trailheads.append((r, c))

    print(grid)
    print(trailheads)

    total = 0
    for trailhead in trailheads:
        score = count_paths(grid, trailhead)
        print(f"Trailhead: {trailhead}, score: {score}")
        total += score

    print(total)

if __name__ == "__main__":
    main(sys.argv[1])