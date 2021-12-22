import sys
from typing import Tuple, Dict, List
from collections import Counter, defaultdict
from itertools import cycle, product
from dataclasses import dataclass

@dataclass
class Universe:
    score: int
    count: int

@dataclass
class Player:
    pos: int
    score: int

def load_data(input_path: str) -> Tuple[int, int]:
    with open(input_path, 'r') as f:
        return tuple(int(line.strip().split(': ')[1]) for line in f)


def finished(round: Dict[int, Universe]) -> bool:
    return all(u.score >= 21 for u in round.values())


def simulate(rolls: Dict[int, int], start: int):
    rounds = []

    round: Dict[int, Universe] = {start: Universe(score=0, count=0)}
    rounds = [round]
    while len(rounds) <= 21:
        next_round: Dict[int, Universe] = defaultdict(lambda: Universe(score=0, count=0))
        for pos, universe in round.items():
            for move, freq in rolls.items():
                next_round[(pos + move) % 10].count += freq

        rounds.append(next_round)
        round = next_round
        print(rounds)

    return rounds

def part2(input_path: str):
    pos1, pos2 = load_data(input_path)
    print(pos1, pos2)
    pos1 -= 1
    pos2 -= 1
    counts = Counter()
    for combo in product([1,2,3], [1,2,3], [1,2,3]):
        counts[sum(combo)] += 1

    p1_wins = 0
    p2_wins = 0
    # Map between the (current board positions, score) and the number of
    # universes that produce this state
    universes = {(pos1, pos2, 0, 0): 1}
    round = 1
    while universes:
        new_universes = Counter()
        print(f'Round: {round}')
        for state, state_freq in universes.items():
            p1_pos, p2_pos, p1_score, p2_score = state
            for p1_roll, roll1_freq in counts.items():
                new_p1_pos = (p1_pos + p1_roll) % 10
                new_p1_score = p1_score + (new_p1_pos + 1)

                if new_p1_score >= 21:
                    p1_wins += state_freq * roll1_freq
                    continue

                for p2_roll, roll2_freq in counts.items():
                    new_p2_pos = (p2_pos + p2_roll) % 10
                    new_p2_score = p2_score + (new_p2_pos + 1)

                    new_state_freq = state_freq * roll1_freq * roll2_freq
                    if new_p2_score >= 21:
                        p2_wins += new_state_freq
                    else:
                        new_state = (
                            new_p1_pos,
                            new_p2_pos,
                            new_p1_score,
                            new_p2_score
                        )
                        new_universes[new_state] += new_state_freq
        universes = new_universes
        round += 1

    print(f'p1 wins: {p1_wins}, p2 wins: {p2_wins}')


def part1(input_path: str):
    pos1, pos2 = load_data(input_path)
    pos1 -= 1
    pos2 -= 1

    score1 = 0
    score2 = 0
    print(pos1, pos2)

    rolls = 0
    die = cycle(range(1, 101))
    while True:
        p1_rolls = next(die) + next(die) + next(die)
        pos1 = (pos1 + p1_rolls) % 10
        score1 += (pos1 + 1)
        rolls += 3
        print(f'Player 1 rolls {p1_rolls} and moves to space {pos1} for a total of {score1}')
        if score1 >= 1000:
            break

        p2_rolls = next(die) + next(die) + next(die)
        pos2 = (pos2 + p2_rolls) % 10
        score2 += (pos2 + 1)
        rolls += 3
        print(f'Player 2 rolls {p2_rolls} and moves to space {pos2} for a total of {score2}')
        if score2 >= 1000:
            break

    losing_score = min(score1, score2)

    result = rolls * losing_score
    print(f'rolls: {rolls}, losing_score: {losing_score}, result: {result}')


if __name__ == '__main__':
    part2(sys.argv[1])