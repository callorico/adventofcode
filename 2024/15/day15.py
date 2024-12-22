import sys
from typing import List, Tuple


def load_data(input_path: str) -> Tuple[List[List[str]], str]:
    grid: List[List[str]] = []
    with open(input_path, "rt") as f:
        for line in f:
            clean = line.strip()
            if not clean:
                break
            grid.append(list(clean))

        moves = "".join(line.strip() for line in f if line.strip())

    return grid, moves


def move(grid: List[List[str]], robot_pos: Tuple[int, int], delta: Tuple[int, int]) -> Tuple[int, int]:
    round = 1
    shifted = []
    row, col = robot_pos
    can_move = False
    while True:
        current = grid[row][col]
        row = robot_pos[0] + (round * delta[0])
        col = robot_pos[1] + (round * delta[1])
        shifted.append((row, col, current))
        if grid[row][col] == ".":
            # Move is possible
            can_move = True
            break

        if grid[row][col] == "#":
            # Move not possible
            break

        round += 1

    if can_move:
        # Previous robot position is now empty
        grid[robot_pos[0]][robot_pos[1]] = "."

        # Everything else shifts over
        for r, c, value in shifted:
            grid[r][c] = value

        new_robot_row, new_robot_col, _ = shifted[0]
        robot_pos = (new_robot_row, new_robot_col)

    return robot_pos


def print_grid(grid: List[List[str]]):
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            print(grid[r][c], end="")
        print()


def main(input_path: str):
    grid, moves = load_data(input_path)

    robot_pos = None
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == "@":
                robot_pos = (r, c)
                break
    assert robot_pos is not None

    print(f"Grid before. Robot at: {robot_pos}")
    print_grid(grid)

    for m in moves:
        if m == "<":
            robot_pos = move(grid, robot_pos, (0, -1))
        elif m == ">":
            robot_pos = move(grid, robot_pos, (0, 1))
        elif m == "^":
            robot_pos = move(grid, robot_pos, (-1, 0))
        elif m == "v":
            robot_pos = move(grid, robot_pos, (1, 0))
        else:
            raise ValueError(f"Unknown move: {m}")

    print(f"Grid after moves. Robot at: {robot_pos}")
    print_grid(grid)

    # Score
    total_gps_coords = 0
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == "O":
                total_gps_coords += (100 * r) + c

    print(total_gps_coords)




if __name__ == "__main__":
    main(sys.argv[1])