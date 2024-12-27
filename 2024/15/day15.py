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
    frontier = [robot_pos]
    shifted = []
    can_move = True
    while frontier:
        row, col = frontier.pop()
        val = grid[row][col]
        assert val == "@" or val == "[" or val == "]"

        new_row = row + delta[0]
        new_col = col + delta[1]
        shifted.append((row, col, new_row, new_col, val))

        new_val = grid[new_row][new_col]
        if new_val == "#":
            # Blocked
            can_move = False
            break
        elif new_val == ".":
            # Allowed
            pass
        else:
            frontier.append((new_row, new_col))
            if new_val == "[" and delta[0] != 0:
                frontier.append((new_row, new_col + 1))
            elif new_val == "]" and delta[0] != 0:
                frontier.append((new_row, new_col - 1))


    if can_move:
        # Clear out all original positions first
        for old_row, old_col, _, _, _ in shifted:
            grid[old_row][old_col] = "."

        # Everything else shifts over
        for _, _, new_row, new_col, value in shifted:
            grid[new_row][new_col] = value

        _, _, new_robot_row, new_robot_col, _ = shifted[0]
        robot_pos = (new_robot_row, new_robot_col)

    return robot_pos


def print_grid(grid: List[List[str]]):
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            print(grid[r][c], end="")
        print()


def expand_grid(grid: List[List[str]]) -> List[List[str]]:
    new_grid = []
    for row in grid:
        new_row = []
        for cell in row:
            if cell == "#":
                new_row.extend(["#", "#"])
            elif cell == "O":
                new_row.extend(["[", "]"])
            elif cell == ".":
                new_row.extend([".", "."])
            elif cell == "@":
                new_row.extend(["@", "."])
            else:
                new_row.append(cell)
        new_grid.append(new_row)

    return new_grid


def main(input_path: str):
    grid, moves = load_data(input_path)
    grid = expand_grid(grid)

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
        #print(f"Moved {m}")
        #print_grid(grid)

    print(f"Grid after moves. Robot at: {robot_pos}")
    print_grid(grid)

    # Score
    total_gps_coords = 0
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == "[":
                total_gps_coords += (100 * r) + c

    print(total_gps_coords)




if __name__ == "__main__":
    main(sys.argv[1])