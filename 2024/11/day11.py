import sys
from typing import List, Dict, Tuple
from collections import defaultdict


def load_data(input_path) -> List[int]:
    with open(input_path, "rt") as f:
        return [int(s) for s in f.read().strip().split(" ")]


def apply_rules(stone: int) -> List[int]:
    new_stones = []
    if stone == 0:
        return [1]

    converted = str(stone)
    if len(converted) % 2 == 0:
        mid = len(converted) // 2
        return [int(converted[:mid]), int(converted[mid:])]

    return [stone * 2024]


def num_stones(stone: int, rounds: int, cache: Dict[int, Dict[int, int]]) -> int:
    if rounds == 0:
        return 1

    precomputed = cache.get((stone, rounds))
    if precomputed is not None:
        return precomputed

    total = 0
    for s in apply_rules(stone):
        total += num_stones(s, rounds-1, cache)

    cache[(stone, rounds)] = total

    return total


def main(input_path):
    stones = load_data(input_path)

    # Part 1
    #rounds = 25
    rounds = 75

    cache: Dict[Tuple[int, int], int] = {}
    total = 0
    for s in stones:
        total += num_stones(s, rounds, cache)

    print(total)


if __name__ == "__main__":
    main(sys.argv[1])
