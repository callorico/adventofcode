import sys
from typing import List, Tuple
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

def main(input_path: str):
    coords = load_data(input_path)

    # grid_size = 7
    # falling_bytes = 12

    grid_size = 71
    falling_bytes = 1024

    start = (0, 0)
    end = (grid_size - 1, grid_size - 1)

    obstacles = set(coords[:falling_bytes])
    print_grid(grid_size, obstacles)

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

    print(best_score[end])




if __name__ == "__main__":
    main(sys.argv[1])
