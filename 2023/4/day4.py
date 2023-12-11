from typing import Iterable, Tuple
from collections import Counter, defaultdict
import sys
import re


def parse_numbers(number_text: str) -> list[int]:
    return [int(v) for v in re.split(r"\s+", number_text) if v]

def load_data(input_path) -> Iterable[Tuple[int, list[int], list[int]]]:
    with open(input_path, "r") as f:
        for line in f.readlines():
            card, numbers = line.strip().split(":", 1)
            _, card_num_text = card.split(" ", 1)
            card_num = int(card_num_text)
            left, right = numbers.split("|", 1)
            winners = parse_numbers(left)
            in_hand = parse_numbers(right)

            yield card_num, winners, in_hand


def main(input_path):
    card_counts: dict[int, int] = defaultdict(lambda: 1)
    for card_num, winners, in_hand in load_data(input_path):
        # How many cards of this number do we have
        card_count = card_counts[card_num]

        winner_set = set(winners)
        counts = Counter(in_hand)
        total_matches = 0
        for val, count in counts.items():
            if val in winner_set:
                total_matches += count

        for card_nums in range(card_num + 1, card_num + total_matches + 1):
            card_counts[card_nums] += card_count

    total_cards = sum(card_counts.values())
    print(card_counts)
    print(total_cards)


if __name__ == "__main__":
    main(sys.argv[1])