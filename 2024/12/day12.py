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
                p = perimeter(region)
                price = a * p
                print(f"A region of {plant} plants with price {a} * {p}: {price}")
                total_price += price

    print(total_price)


if __name__ == "__main__":
    main(sys.argv[1])