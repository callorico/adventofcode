import sys
import re
from typing import Tuple, List, Optional
from dataclasses import dataclass
from itertools import product


@dataclass
class GameConfig:
    a_delta: Tuple[int, int]
    b_delta: Tuple[int, int]
    target: Tuple[int, int]


def parse_numbers(line: str) -> Tuple[int, int]:
    matches = re.findall(r"(\d+)", line)
    assert len(matches) == 2
    return tuple(int(d) for d in matches)


def load_data(input_path: str) -> List[GameConfig]:
    games: List[GameConfig] = []
    with open(input_path, "rt") as f:
        try:
            while button_a_line := next(f):
                button_b_line = next(f)
                target = next(f)
                # Eat blank line between games
                next(f)

                games.append(
                    GameConfig(
                        a_delta=parse_numbers(button_a_line),
                        b_delta=parse_numbers(button_b_line),
                        target=parse_numbers(target)
                    )
                )
        except StopIteration:
            pass

    return games


def main(input_path: str):
    games = load_data(input_path)

    # it costs 3 tokens to push the A button and 1 token to push the B button.
    total_tokens = 0
    for g in games:
        best_cost: Optional[int] = None
        for a, b in product(range(1, 101), repeat=2):
            x = g.a_delta[0] * a + g.b_delta[0] * b
            y = g.a_delta[1] * a + g.b_delta[1] * b

            if x == g.target[0] and y == g.target[1]:
                potential_cost = 3 * a + b
                #print(f"A button presses: {a}, B button presses: {b}")
                if best_cost is None or potential_cost < best_cost:
                    best_cost = potential_cost

        if best_cost is not None:
            total_tokens += best_cost

    print(total_tokens)


if __name__ == "__main__":
    main(sys.argv[1])
