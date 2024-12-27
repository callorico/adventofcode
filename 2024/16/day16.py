import sys
from typing import List, Dict, Tuple


DIRECTIONS = (
    # N
    (-1, 0),
    # S
    (1, 0),
    # E
    (0, 1),
    # W
    (0, -1),
)


def load_data(input_path: str) -> List[str]:
    maze = []
    with open(input_path, "rt") as f:
        for line in f:
            cleaned = line.strip()
            if cleaned:
                maze.append(cleaned)

    return maze


def main(input_path: str):
    maze = load_data(input_path)

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

    lowest_score: Dict[Tuple[int, int], int] = {}

    east = (0, 1)
    next_state = [(start, east, 0)]
    while next_state:
        pos, dir, score = next_state.pop()
        row, col = pos
        if maze[row][col] == "#":
            continue

        if pos in lowest_score and lowest_score[pos] < score:
            continue

        # Best path to this node seen so far
        lowest_score[pos] = score

        if maze[row][col] == "E":
            continue

        # Try all possible moves
        for new_dir in DIRECTIONS:
            new_position = (row + new_dir[0], col + new_dir[1])
            new_score = score + 1
            if dir != new_dir:
                new_score += 1000

            next_state.append((new_position, new_dir, new_score))

    print(lowest_score[end])


if __name__ == "__main__":
    main(sys.argv[1])

