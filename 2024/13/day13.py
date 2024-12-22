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
        while button_a_line := next(f, None):
            button_b_line = next(f)
            target = next(f)
            games.append(
                GameConfig(
                    a_delta=parse_numbers(button_a_line),
                    b_delta=parse_numbers(button_b_line),
                    target=parse_numbers(target)
                )
            )
            # Eat blank line between games
            next(f, None)


    return games


def main(input_path: str):
    games = load_data(input_path)
    print(len(games))

    # Modification for part 2
    factor = 10000000000000
    for g in games:
        g.target = (g.target[0] + factor, g.target[1] + factor)

    total_tokens = 0
    for g in games:
        print(g)
        a_factor = (g.a_delta[0] * g.b_delta[1]) - (g.a_delta[1] * g.b_delta[0])
        x = (g.target[0] * g.b_delta[1]) - (g.target[1] * g.b_delta[0])

        a_presses, mod = divmod(x, a_factor)
        if mod == 0:
            # Calculate number of b presses now
            b_presses, mod = divmod(g.target[0] - (g.a_delta[0] * a_presses), g.b_delta[0])
            if mod == 0 and a_presses > 0 and b_presses > 0:
                print(f"Solution: {a_presses},{b_presses}")
                # it costs 3 tokens to push the A button and 1 token to push the B button.
                cost = a_presses * 3 + b_presses
                total_tokens += cost


    print(total_tokens)


if __name__ == "__main__":
    main(sys.argv[1])
