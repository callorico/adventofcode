import sys
from typing import List
from collections import Counter


def load_data(input_path: str) -> List[str]:
    with open(input_path, 'r') as f:
        return [int(c) for c in f.readline().split(',')]


def part1(fish: List[int]) -> int:
    for day in range(80):
        new_fish = 0
        next_fish = []
        for age in fish:
            new_age = age - 1
            if new_age < 0:
                new_age = 6
                new_fish += 1
            next_fish.append(new_age)

        next_fish.extend([8] * new_fish)
        #print(f'Day {day+1}: {next_fish}')
        fish = next_fish

    return len(fish)


def part2(fish: List[int]) -> int:
    counts = Counter()
    for age in fish:
        counts[age] += 1

    for day in range(256):
        new_counts = Counter()
        for age, count in counts.items():
            new_age = age - 1
            if new_age < 0:
                new_counts[6] += count
                new_counts[8] += count
            else:
                new_counts[new_age] += count

        counts = new_counts

    return sum(v for v in counts.values())


def main(input_path: str):
    fish = load_data(input_path)
    print(fish)

    total = part2(fish)
    print(f'Total fish: {total}')


if __name__ == '__main__':
    main(sys.argv[1])