import sys
from typing import Counter, List, Tuple, Iterable, Dict, Set
from collections import defaultdict

SignalPattern = Tuple[List[str], List[str]]

def load_data(input_path: str) -> Iterable[SignalPattern]:
    with open(input_path, 'r') as f:
        for line in f:
            raw_signal, raw_pattern = line.split(' | ')
            signals = [s.strip() for s in raw_signal.split(' ')]
            pattern = [p.strip() for p in raw_pattern.split(' ')]
            yield signals, pattern

def part1(input_path: str):
    # 1: 2 segments
    # 4: 4 segments
    # 7: 3 segments
    # 8: 7 segments
    targets = set([2, 4, 3, 7])

    total = 0
    for _, patterns in load_data(input_path):
        for pattern in patterns:
            if len(pattern) in targets:
                total += 1

    print(total)

def canonical_signal(signal: Iterable[str]) -> str:
    return ''.join(sorted(signal))

def part2(input_path: str):
    total = 0
    for signals, patterns in load_data(input_path):
        assert(len(signals) == 10)

        counts: Dict[int, List[Set[str]]] = defaultdict(list)
        for signal in signals:
            counts[len(signal)].append(set(signal))

        # map between the canonical scrambled mapping and the digit
        mapping: Dict[str, int] = {}

        # The easy ones
        one = counts[2][0]
        seven = counts[3][0]
        four = counts[4][0]
        eight = counts[7][0]

        mapping[canonical_signal(one)] = 1
        mapping[canonical_signal(seven)] = 7
        mapping[canonical_signal(four)] = 4
        mapping[canonical_signal(eight)] = 8

        # 6 edges: 0, 6, 9
        six_edges = counts[6]
        nine = next(s for s in six_edges if s.issuperset(four))
        mapping[canonical_signal(nine)] = 9
        six_edges.remove(nine)
        assert(len(six_edges) == 2)

        zero = next(s for s in six_edges if s.issuperset(one))
        mapping[canonical_signal(zero)] = 0
        six_edges.remove(zero)
        assert(len(six_edges) == 1)

        six = six_edges.pop()
        mapping[canonical_signal(six)] = 6
        assert(len(six_edges) == 0)

        # 5 edges: 2, 3, 5
        five_edges = counts[5]
        three = next(s for s in five_edges if s.issuperset(one))
        mapping[canonical_signal(three)] = 3
        five_edges.remove(three)
        assert(len(five_edges) == 2)

        two = next(s for s in five_edges if len(four.difference(s)) == 2)
        mapping[canonical_signal(two)] = 2
        five_edges.remove(two)
        assert(len(five_edges) == 1)

        five = five_edges.pop()
        mapping[canonical_signal(five)] = 5
        assert(len(five_edges) == 0)

        assert(len(patterns) == 4)
        digits = [str(mapping[canonical_signal(p)]) for p in patterns]
        total += int(''.join(digits))

    print(total)



if __name__ == '__main__':
    part2(sys.argv[1])