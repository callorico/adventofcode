import sys
from typing import Tuple, List, Dict, Set
from collections import Counter

def load_data(input_path: str) -> Tuple[str, Dict[str, str]]:
    with open(input_path, 'r') as f:
        template = f.readline().strip()
        f.readline()

        pairs = (line.strip().split(' -> ') for line in f)
        pair_insertion_rules = {k: v for k, v in pairs}

        return template, pair_insertion_rules


def part2(input_path: str):
    template, rules = load_data(input_path)

    letter_counts: Counter = Counter()
    for c in template:
        letter_counts[c] += 1

    current_pairs: Counter = Counter()
    for index in range(len(template) - 1):
        pair = template[index:index+2]
        current_pairs[pair] += 1

    print(f'Template: {template}. letter_counts: {letter_counts}')

    for round in range(40):
        new_current_pairs: Counter = Counter()
        for pair, count in current_pairs.items():
            # print(current_pairs)
            insert = rules[pair]
            letter_counts[insert] += count

            # Split into two pairs
            pair1 = pair[0] + insert
            pair2 = insert + pair[1]

            new_current_pairs[pair1] += count
            new_current_pairs[pair2] += count

        current_pairs = new_current_pairs

    print(letter_counts)

    freq = letter_counts.most_common()
    most_common = freq[0]
    least_common = freq[-1]
    print(most_common)
    print(least_common)

    answer: int = most_common[1] - least_common[1]
    print(answer)


def part1(input_path: str):
    template, rules = load_data(input_path)

    polymer = template
    for round in range(10):
        new_polymer: List[str] = [polymer[0]]
        for index in range(len(polymer) - 1):
            segment = polymer[index:index+2]
            replacement = rules[segment]
            new_polymer.extend((replacement, segment[1]))

        polymer = ''.join(new_polymer)
        print(f'After round {round+1}: {polymer}')

    counts: Counter = Counter()
    for c in polymer:
        counts[c] += 1

    freq = counts.most_common()
    most_common = freq[0]
    least_common = freq[-1]
    print(most_common)
    print(least_common)

    answer: int = most_common[1] - least_common[1]
    print(answer)


if __name__ == '__main__':
    part2(sys.argv[1])