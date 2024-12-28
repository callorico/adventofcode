import sys
from typing import List, Dict, Tuple, Set
import heapq


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


def print_maze(maze: List[str], visited: Set[Tuple[int, int]]):
    for r in range(len(maze)):
        for c in range(len(maze[0])):
            if (r, c) in visited:
                print("O", end="")
            else:
                print(maze[r][c], end="")
        print()


def main(input_path: str):
    maze = load_data(input_path)

    start, end = find_endpoints(maze)
    east = (0, 1)
    print(f"Start: {start}, dir: {east}, end: {end}")
    frontier = [(0, start, east, set())]
    heapq.heapify(frontier)

    # Tracks the best score seen so far when heading in a particular direction
    best_score: Dict[Tuple[Tuple[int, int], Tuple[int, int]], int] = {}

    best_overall_score = None
    all_visited = set()
    while frontier:
        score, pos, dir, visited = heapq.heappop(frontier)
        new_visited = set(visited)
        new_visited.add(pos)

        best_score[(pos, dir)] = score
        row, col = pos
        #print(f"{pos}, {dir} core: {score}")

        if pos == end:
            # Record successful path and keep going if the score is better or as good as
            # what we have previously seen. Don't break out of the loop yet though
            # since there could be multiple paths that end with the same score
            if best_overall_score is None or score < best_overall_score:
                best_overall_score = score
                all_visited.clear()

            if best_overall_score == score:
                all_visited.update(new_visited)
            continue

        opposite = (dir[0] * -1, dir[1] * -1)
        for new_dir in DIRECTIONS:
            if new_dir == opposite:
                # No point in heading in the direction we
                # just came from. That is strictly worse.
                continue

            new_position = (row + new_dir[0], col + new_dir[1])
            if maze[new_position[0]][new_position[1]] == "#":
                continue

            new_score = score + 1
            if dir != new_dir:
                new_score += 1000

            best_so_far = best_score.get((new_position, new_dir))
            if best_so_far is not None and best_so_far < new_score:
                # Abandon this path as it is strictly worse
                continue

            heapq.heappush(frontier, (new_score, new_position, new_dir, new_visited))

    print_maze(maze, all_visited)
    print(len(all_visited))


if __name__ == "__main__":
    main(sys.argv[1])
