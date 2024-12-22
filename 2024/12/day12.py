import sys
from typing import List, Dict, Set, Tuple


def load_data(input_path: str) -> List[str]:
    with open(input_path, "rt") as f:
        return [line.strip() for line in f if line.strip()]


def find_region(grid: List[str], visited: Set[Tuple[int, int]], row: int, col: int, plant: str) -> List[Tuple[int, int]]:
    if row < 0 or row >= len(grid):
        return []

    if col < 0 or col >= len(grid[0]):
        return []

    if grid[row][col] != plant:
        return []

    coord = (row, col)
    if coord in visited:
        return []

    visited.add(coord)
    region = [coord]
    region.extend(find_region(grid, visited, row-1, col, plant))
    region.extend(find_region(grid, visited, row+1, col, plant))
    region.extend(find_region(grid, visited, row, col-1, plant))
    region.extend(find_region(grid, visited, row, col+1, plant))

    return region


def perimeter(region: List[Tuple[int, int]]) -> int:
    lookup = set(region)
    total = 0
    for cell in region:
        # Each cell contributes 4 - # of neighbors to the perimeter
        r, c = cell
        cell_perimeter = 4
        cell_perimeter -= int((r-1, c) in lookup)
        cell_perimeter -= int((r+1, c) in lookup)
        cell_perimeter -= int((r, c-1) in lookup)
        cell_perimeter -= int((r, c+1) in lookup)

        total += cell_perimeter
    return total


def sides(region: List[Tuple[int, int]]) -> int:
    area_lookup: Set[Tuple[int, int]]= set(region)
    first = region[0]
    min_row = max_row = first[0]
    min_col = max_col = first[1]

    for r, c in region[1:]:
        if r < min_row:
            min_row = r
        elif r > max_row:
            max_row = r

        if c < min_col:
            min_col = c
        elif c > max_col:
            max_col = c

    #print(f"Region: {area_lookup}")
    #print(f"Region bounds: [{min_row},{min_col}] to [{max_row},{max_col}]")

    # Idea: Iterate through grid in horizontal lines and
    # vertical lines and count # of contiguous segments

    total_sides = 0
    # Iterate through all the horizontal lines and
    # count sides above and below
    within_above_side = False
    within_below_side = False
    for r in range(min_row, max_row + 1):
        # Extend one column out past the right edge of the region to terminate
        # any sides that extend to the end.
        for c in range(min_col, max_col + 2):
            in_region = (r, c) in area_lookup
            if in_region:
                # Check above
                if (r-1, c) in area_lookup:
                    if within_above_side:
                        total_sides += 1
                    within_above_side = False
                else:
                    within_above_side = True

                # Check below
                if (r+1, c) in area_lookup:
                    if within_below_side:
                        total_sides += 1
                    within_below_side = False
                else:
                    within_below_side = True
            else:
                # Any currently active side is ended
                if within_above_side:
                    total_sides += 1
                within_above_side = False

                if within_below_side:
                    total_sides += 1
                within_below_side = False


    # Iterate through all the vertical lines and count
    # sides to the left and right
    within_left_side = False
    within_right_side = False
    for c in range(min_col, max_col + 1):
        # Extend one row out past the bottom edge of the region to terminate
        # any sides that extend to the bottom
        for r in range(min_row, max_row + 2):
            in_region = (r, c) in area_lookup
            if in_region:
                # Check left
                if (r, c-1) in area_lookup:
                    if within_left_side:
                        total_sides += 1
                    within_left_side = False
                else:
                    within_left_side = True

                # Check right
                if (r, c+1) in area_lookup:
                    if within_right_side:
                        total_sides += 1
                    within_right_side = False
                else:
                    within_right_side = True
            else:
                # Any currently active side is ended
                if within_left_side:
                    total_sides += 1
                within_left_side = False

                if within_right_side:
                    total_sides += 1
                within_right_side = False

    return total_sides


def area(region: List[Tuple[int, int]]) -> int:
    return len(region)


def main(input_path):
    grid = load_data(input_path)

    visited: Set[Tuple[int, int]] = set()

    total_price = 0
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            plant = grid[r][c]
            if (r, c) not in visited:
                region = find_region(grid, visited, r, c, plant)
                a = area(region)
                # Part 1
                #p = perimeter(region)
                #price = a * p
                # Part 2
                s = sides(region)
                price = a * s
                print(f"A region of {plant} plants with price {a} * {s}: {price}")
                total_price += price

    print(total_price)


if __name__ == "__main__":
    main(sys.argv[1])