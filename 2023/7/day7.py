import sys
from typing import Tuple
from dataclasses import dataclass
from functools import total_ordering
from collections import Counter
from enum import IntEnum


class HandType(IntEnum):
    FIVE_OF_A_KIND = 100
    FOUR_OF_A_KIND = 90
    FULL_HOUSE = 80
    THREE_OF_A_KIND = 70
    TWO_PAIR = 60
    ONE_PAIR = 50
    HIGH_CARD = 40


CARD_VALUES: dict[str, int] = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
    "J": 1,
}


@total_ordering
class Hand:
    def __init__(self, cards: str):
        assert len(cards) == 5
        self.cards = cards
        counts = Counter(cards)
        try:
            joker_count = counts.pop("J")
        except KeyError:
            pass
        else:
            top_match = counts.most_common(1)
            if not top_match:
                # The all-joker edge case
                counts["A"] = joker_count
            else:
                counts[top_match[0][0]] += joker_count

        matches = counts.most_common(2)

        if len(matches) == 1:
            self.hand_type = HandType.FIVE_OF_A_KIND
        else:
            count = matches[0][1]
            if count == 4:
                self.hand_type = HandType.FOUR_OF_A_KIND
            elif count == 3:
                if matches[1][1] == 2:
                    self.hand_type = HandType.FULL_HOUSE
                else:
                    # three of a kind
                    self.hand_type = HandType.THREE_OF_A_KIND
            elif count == 2:
                if matches[1][1] == 2:
                    self.hand_type = HandType.TWO_PAIR
                else:
                    self.hand_type = HandType.ONE_PAIR
            else:
                self.hand_type = HandType.HIGH_CARD

        self.card_values = tuple(CARD_VALUES[c] for c in cards)

    def __lt__(self, other):
        return (self.hand_type, self.card_values) < (other.hand_type, other.card_values)
    
    def __repr__(self):
        return f"{self.cards} ({self.hand_type.name})"


def load_data(input_path) -> list[Tuple[Hand, int]]:
    hands = []
    with open(input_path, "r") as f:
        for line in f:
            hand_raw = line.strip()
            if not hand_raw:
                continue

            print(f"Raw hand: {hand_raw}")
            cards, bid = hand_raw.split(" ")
            hands.append((Hand(cards), int(bid)))

    return hands


def main(input_path):
    hands: list[Tuple[Hand, int]] = load_data(input_path)
    ordered = sorted(hands, key=lambda k: k[0])

    total = 0
    for rank, hand in enumerate(ordered):
        total += (rank + 1) * hand[1]

    print(ordered)
    print(total)


if __name__ == "__main__":
    main(sys.argv[1])