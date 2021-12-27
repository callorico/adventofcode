import sys
from typing import List


def load_data(input_path: str) -> List[str]:
    with open(input_path, 'r') as f:
        return [line.strip() for line in f]


def part1(input_path: str):
    state = load_data(input_path)
    south_cucumbers = set()
    east_cucumbers = set()

    rows = len(state)
    cols = len(state[0])

    # Store cucumber positions
    for r in range(rows):
        for c in range(cols):
            if state[r][c] == '>':
                east_cucumbers.add((r, c))
            elif state[r][c] == 'v':
                south_cucumbers.add((r, c))

    step = 0
    while True:
        # First move east
        next_east_cucumbers = set()
        next_south_cucumbers = set()
        for r, c in east_cucumbers:
            next_pos = (r, (c + 1) % cols)
            if (next_pos not in east_cucumbers and
                    next_pos not in south_cucumbers):
                next_east_cucumbers.add(next_pos)
            else:
                next_east_cucumbers.add((r, c))

        for r, c in south_cucumbers:
            next_pos = ((r + 1) % rows, c)
            if (next_pos not in next_east_cucumbers and
                    next_pos not in south_cucumbers):
                next_south_cucumbers.add(next_pos)
            else:
                next_south_cucumbers.add((r, c))

        assert len(east_cucumbers) == len(next_east_cucumbers)
        assert len(south_cucumbers) == len(next_south_cucumbers)
        step += 1

        if (east_cucumbers == next_east_cucumbers and
                south_cucumbers == next_south_cucumbers):
            # No movement
            break

        east_cucumbers = next_east_cucumbers
        south_cucumbers = next_south_cucumbers

    print(f'Stopped moving after {step} steps')


if __name__ == '__main__':
    part1(sys.argv[1])
