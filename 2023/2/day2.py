from typing import Dict
from collections import defaultdict
import sys
from dataclasses import dataclass

@dataclass
class Game:
    id: int
    counts: Dict[str, int]

COLORS = {"green", "red", "blue"}

def load_data(input_path) -> list[Game]:
    with open(input_path, "r") as f:
        games: list[Game] = []
        for line in f:
            game, results = line.strip().split(": ", 1)
            id = int(game.split(" ")[1])
            rounds = results.split("; ")
            counts: Dict[str, int] = defaultdict(int)
            for r in rounds:
                cubes = r.split(", ")
                for c in cubes:
                    count_raw, color = c.split(" ")
                    assert color in COLORS, "Parsed invalid color: f{color} from raw line f{line}"
                    counts[color] = max(counts[color], int(count_raw))


            games.append(Game(id=id, counts=counts))

        return games


def part1(games: list[Game]) -> int:
    id_sum = 0
    for g in games:
        if g.counts["red"] <= 12 and g.counts["green"] <= 13 and g.counts["blue"] <= 14:
            id_sum += g.id

    return id_sum


def main(input_path):
    games = load_data(input_path)
    print(part1(games))


if __name__ == "__main__":
    main(sys.argv[1])