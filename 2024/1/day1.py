import sys
from typing import Dict, Tuple, List
from collections import Counter

def load_data(input_path: str) -> Tuple[List[int], List[int]]:
    left: List[int] = []
    right: List[int] = []
    with open(input_path, 'r') as f:
        for line in f:
            tokens = line.split(" ", 1)
            if len(tokens) == 2:
                left.append(int(tokens[0]))
                right.append(int(tokens[1]))

    return left, right


def part1(input_path):
    left, right = load_data(input_path)
    left.sort()
    right.sort()

    distance = sum(abs(x - y) for x, y in zip(left, right))
    print(distance)

def part2(input_path):
    left, right = load_data(input_path)

    counts = Counter()
    for x in right:
        counts[x] += 1

    similarity = sum(x * counts[x] for x in left)
    print(similarity)


def main(input_path):
    part1(input_path)

    part2(input_path)


if __name__ == '__main__':
    main(sys.argv[1])
