from typing import Iterable, Tuple
from collections import Counter
import sys
import re


def parse_numbers(number_text: str) -> list[int]:
    return [int(v) for v in re.split(r"\s+", number_text) if v]

def load_data(input_path) -> Iterable[Tuple[list[int], list[int]]]:
    with open(input_path, "r") as f:
        for line in f.readlines():
            card, numbers = line.strip().split(":", 1)
            left, right = numbers.split("|", 1)
            winners = parse_numbers(left)
            in_hand = parse_numbers(right)

            yield winners, in_hand



def main(input_path):
    total = 0 

    for winners, in_hand in load_data(input_path):
        winner_set = set(winners)
        counts = Counter(in_hand)
        total_matches = 0
        for val, count in counts.items():
            if val in winner_set:
                total_matches += count


        if total_matches > 0:
            total += pow(2, total_matches - 1)

    print(total)


if __name__ == "__main__":
    main(sys.argv[1])