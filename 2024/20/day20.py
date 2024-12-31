import sys
from typing import List, Tuple, Optional, Set
import heapq
from collections import defaultdict


def load_data(input_path: str) -> List[str]:
    maze = []
    with open(input_path, "rt") as f:
        for line in f:
            cleaned = line.strip()
            if cleaned:
                maze.append(cleaned)

    return maze


def find_endpoints(maze: List[str]) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    start = None
    end = None
    for r in range(len(maze)):
        for c in range(len(maze[0])):
            if maze[r][c] == "S":
                start = (r, c)
            elif maze[r][c] == "E":
                end = (r, c)

    assert start is not None
    assert end is not None

    return start, end


DIRECTIONS = (
    # Up
    (-1, 0),
    # Down
    (1, 0),
    # Left
    (0, -1),
    # Right
    (0, 1),
)


def print_maze(maze: List[str]):
    for r in maze:
        print(r)


def best_path(maze: List[str], start: Tuple[int, int], end: Tuple[int, int]) -> int:
    frontier = [(0, start)]
    best_score = {}
    heapq.heapify(frontier)
    while frontier:
        score, pos = heapq.heappop(frontier)

        if pos in best_score and best_score[pos] <= score:
            # No point in continuing on this path
            continue

        best_score[pos] = score
        # print(f"{pos}: {score}")

        if pos == end:
            break

        # Next positions
        for dir in DIRECTIONS:
            next_pos = (pos[0] + dir[0], pos[1] + dir[1])
            if next_pos[0] < 0 or next_pos[0] >= len(maze):
                continue

            if next_pos[1] < 0 or next_pos[1] >= len(maze[0]):
                continue

            if maze[next_pos[0]][next_pos[1]] == "#":
                continue

            new_score = score + 1
            heapq.heappush(frontier, (new_score, next_pos))

    return best_score.get(end)


def cheat_maze(maze: List[str], hole: Tuple[int, int]) -> List[str]:
    copy = []
    hole_row, hole_col = hole
    for r in range(len(maze)):
        row = maze[r]
        if r == hole_row:
            copy.append(row[:hole_col] + "." + row[hole_col+1:])
        else:
            copy.append(row)

    return copy


def main(input_path: str):
    maze = load_data(input_path)
    start, end = find_endpoints(maze)
    print(start, end)
    print(f"rows: {len(maze)}, cols: {len(maze[0])}")

    control_score = best_path(maze, start, end)
    print(control_score)

    # print_maze(maze)

    total = defaultdict(int)
    for r in range(1, len(maze) - 1):
        for c in range(1, len(maze[0]) - 1):
            if maze[r][c] == "#":
                modified = cheat_maze(maze, (r, c))
                score = best_path(modified, start, end)
                diff = control_score - score
                if diff > 0:
                    total[diff] += 1

    total_cheats = 0
    best_savings = sorted(total.items(), key=lambda k: k[0])
    for savings, count in best_savings:
        print(f"{count} cheats that save {savings}")
        if savings >= 100:
            total_cheats += count

    print(total_cheats)


if __name__ == "__main__":
    main(sys.argv[1])