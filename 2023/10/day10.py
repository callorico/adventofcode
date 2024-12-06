import sys
from typing import Tuple


def load_data(input_path) -> Tuple[list[str], Tuple[int, int]]:
    grid = []
    with open(input_path, "r") as f:
        start_row = None
        start_col = None
        for line in f:
            if start_col is None:
                index = line.find("S")
                if index != -1:
                    start_col = index
                    start_row = len(grid)
            grid.append(line.strip())

    assert start_row is not None
    assert start_col is not None

    return grid, (start_row, start_col)

# | is a vertical pipe connecting north and south.
# - is a horizontal pipe connecting east and west.
# L is a 90-degree bend connecting north and east.
# J is a 90-degree bend connecting north and west.
# 7 is a 90-degree bend connecting south and west.
# F is a 90-degree bend connecting south and east.
# . is ground; there is no pipe in this tile.
NORTH = (-1, 0)
SOUTH = (1, 0)
WEST = (0, -1)
EAST = (0, 1)

PIPE_SHAPES = {
    ".": frozenset([]),
    "|": frozenset([NORTH, SOUTH]),
    "-": frozenset([EAST, WEST]),
    "L": frozenset([NORTH, EAST]),
    "J": frozenset([NORTH, WEST]),
    "7": frozenset([SOUTH, WEST]),
    "F": frozenset([SOUTH, EAST]),
    "S": frozenset([NORTH, SOUTH, EAST, WEST]),
}

def can_move(grid: list[str], current_pos: Tuple[int, int], offset: Tuple[int, int]) -> bool:
    current_pipe = grid[current_pos[0]][current_pos[1]]
    dest_pipe = grid[current_pos[0] + offset[0]][current_pos[1] + offset[1]]

    inverted = (-offset[0], -offset[1])
    # Check whether current pipe allows movement in the offset direction and
    # that the destination pipe accepts incoming flow from the offset direction
    return offset in PIPE_SHAPES[current_pipe] and inverted in PIPE_SHAPES[dest_pipe]


def print_grid(grid: list[str], distances: dict[Tuple[int, int], int]):
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            dist = distances.get((r, c))
            if dist is None:
                ch = grid[r][c]
            else:
                # ch = str(dist)
                ch = "X"
            sys.stdout.write(ch)
        sys.stdout.write("\n")


def in_bounds(grid: list[str], pos: Tuple[int, int]) -> bool:
    num_rows = len(grid)
    num_cols = len(grid[0])

    if pos[0] < 0 or pos[0] >= num_rows:
        return False

    if pos[1] < 0 or pos[1] >= num_cols:
        return False

    return True


def boundary_fill(grid: list[str], filled: set[Tuple[int, int]]):
    num_rows = len(grid)
    num_cols = len(grid[0])

    top_border = [(0, c) for c in range(num_cols)]
    bottom_border = [(num_rows - 1, c) for c in range(num_cols)]
    left_border = [(r, 0) for r in range(num_rows)]
    right_border = [(r, num_cols - 1) for r in range(num_rows)]

    candidates: list[Tuple[int, int]] = top_border + bottom_border + left_border + right_border
    while candidates:
        pos = candidates.pop()
        if pos in filled:
            continue

        filled.add(pos)

        for offset in [NORTH, SOUTH, EAST, WEST]:
            new_pos = (pos[0] + offset[0], pos[1] + offset[1])
            if in_bounds(grid, new_pos):
                candidates.append(new_pos)


def main(input_path):
    grid, start = load_data(input_path)

    move = 0
    distances: dict[Tuple[int, int], int] = {}
    current_pos = [start]


    while current_pos:
        next_pos = []
        for pos in current_pos:
            # print(f"Considering position {pos} on move {move}")
            distances[pos] = move
            for offset in [NORTH, SOUTH, EAST, WEST]:
                potential_next_pos = (pos[0] + offset[0], pos[1] + offset[1])
                if potential_next_pos in distances:
                    continue

                if not in_bounds(grid, potential_next_pos):
                    continue

                if not can_move(grid, pos, offset):
                    continue

                next_pos.append(potential_next_pos)

        # print(f"Grid after move {move}")
        # print_grid(grid, distances)
        # print(f"Valid next moves are {next_pos}")
        current_pos = next_pos
        move += 1

    print_grid(grid, distances)
    print(f"Max distance was {move - 1}")
    print(f"Loop tile count: {len(distances)}")

    # Count all tiles reachable from the boundary
    filled: set[Tuple[int, int]] = set(distances.keys())
    boundary_fill(grid, filled)
    #
    # Then enclosed tiles = total tiles - filled_tiles
    total_tiles = len(grid) * len(grid[0])

    enclosed_tiles = total_tiles - len(filled)
    print(f"Enclosed tiles is {enclosed_tiles}")


if __name__ == "__main__":
    main(sys.argv[1])