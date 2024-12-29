import sys
from typing import List, Tuple, Optional, Set
import heapq


def load_data(input_path: str) -> List[Tuple[int, int]]:
    coords = []
    with open(input_path, "rt") as f:
        for line in f:
            cleaned = line.strip()
            if cleaned:
                coord = tuple(int(t) for t in cleaned.split(",", 1))
                assert len(coord) == 2
                coords.append(coord)

    return coords


def print_grid(grid_size: int, bytes: List[Tuple[int, int]]):
    lookup = set(bytes)
    for y in range(grid_size):
        for x in range(grid_size):
            if (x, y) in bytes:
                print("#", end="")
            else:
                print(".", end="")

        print()


DIRECTIONS = (
    # Up
    (0, -1),
    # Down
    (0, 1),
    # Left
    (-1, 0),
    # Right
    (1, 0),
)


def best_path_length(grid_size: int, obstacles: Set[Tuple[int, int]]) -> Optional[int]:
    start = (0, 0)
    end = (grid_size - 1, grid_size - 1)

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
            if next_pos in obstacles:
                continue

            if next_pos[0] < 0 or next_pos[0] >= grid_size:
                continue

            if next_pos[1] < 0 or next_pos[1] >= grid_size:
                continue

            new_score = score + 1
            heapq.heappush(frontier, (new_score, next_pos))

    return best_score.get(end)


def main(input_path: str):
    coords = load_data(input_path)

    grid_size = 71

    min_falling_bytes = 1024
    max_falling_bytes = len(coords)

    while True:
        curr_range = max_falling_bytes - min_falling_bytes
        if curr_range == 1:
            break

        mid = min_falling_bytes + (curr_range // 2)
        obstacles = set(coords[:mid])
        length = best_path_length(grid_size, obstacles)
        print(f"{min_falling_bytes} - {max_falling_bytes}, Solution: {length}")
        if length is None:
            max_falling_bytes = mid
        else:
            min_falling_bytes = mid

    assert min_falling_bytes + 1 == max_falling_bytes

    obstacles = set(coords[:min_falling_bytes])
    assert best_path_length(grid_size, obstacles) is not None
    print(f"Solution possible at {min_falling_bytes}")

    obstacles = coords[:max_falling_bytes]
    assert best_path_length(grid_size, set(obstacles)) is None
    print(f"Solution not possible at {max_falling_bytes}")

    coord = obstacles[-1]
    print(",".join(str(i) for i in coord))

    # falling_bytes = 1024

    # obstacles = set(coords[:falling_bytes])
    # # print_grid(grid_size, obstacles)

    # # Find the smallest number of obstacles that create an unsolvable grid

    # length = best_path_length(grid_size, set(coords))
    # print(length)


if __name__ == "__main__":
    main(sys.argv[1])
