import sys
from typing import List, Tuple, Dict, Iterable
from collections import defaultdict, Counter
from itertools import combinations


def load_data(input_path: str) -> List[str]:
    grid = []
    with open(input_path, 'rt') as f:
        for line in f:
            cleaned = line.strip()
            if not cleaned:
                break

            grid.append(cleaned)
    return grid


def print_grid(grid: List[str], antinodes: Iterable[Tuple[int, int]]):
    rows = len(grid)
    cols = len(grid[0])
    for r in range(rows):
        for c in range(cols):
            grid_val = grid[r][c]
            if grid_val == "." and (r, c) in antinodes:
                val = "#"
            else:
                val = grid_val
            print(val, end="")
        print()


def in_bounds(grid: List[str], coord: Tuple[int, int]) -> bool:
    rows = len(grid)
    cols = len(grid[0])

    r, c = coord

    return r >= 0 and r < rows and c >=0 and c < cols


def main(input_path):
    grid = load_data(input_path)
    antinodes = set()
    print_grid(grid, antinodes)

    # Group nodes by type
    antenna_positions: Dict[str, List[Tuple[int, int]]] = defaultdict(list)
    rows = len(grid)
    cols = len(grid[0])
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != ".":
                antenna_positions[grid[r][c]].append((r, c))

    print(antenna_positions)

    # Generate antinode positions for all antenna pairs

    for antenna, positions in antenna_positions.items():
        for pair in combinations(positions, 2):
            ant1, ant2 = pair
            slope = (ant1[0] - ant2[0], ant1[1] - ant2[1])
            antinodes.add(ant1)
            antinodes.add(ant2)

            multiple = 1
            while True:
                still_in_bounds = False

                antinode1 = (ant1[0] + (multiple * slope[0]), ant1[1] + (multiple * slope[1]))
                if in_bounds(grid, antinode1):
                    antinodes.add(antinode1)
                    still_in_bounds = True
                antinode2 = (ant2[0] - (multiple * slope[0]), ant2[1] - (multiple * slope[1]))
                if in_bounds(grid, antinode2):
                    antinodes.add(antinode2)
                    still_in_bounds = True

                if not still_in_bounds:
                    # We've extended past the grid boundary in both directions
                    break

                multiple += 1

    print_grid(grid, antinodes)
    total = len(antinodes)
    print(total)


if __name__ == '__main__':
    main(sys.argv[1])
