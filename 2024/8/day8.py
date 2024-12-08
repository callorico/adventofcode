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
            if (r, c) in antinodes:
                val = "#"
            else:
                val = grid[r][c]
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

            antinode1 = (ant1[0] + slope[0], ant1[1] + slope[1])
            antinode2 = (ant2[0] - slope[0], ant2[1] - slope[1])

            print(pair, antinode1, antinode2)

            for antinode in [antinode1, antinode2]:
                if in_bounds(grid, antinode):
                    antinodes.add(antinode)

    total = len(antinodes)
    print(total)

    print_grid(grid, antinodes)


if __name__ == '__main__':
    main(sys.argv[1])
