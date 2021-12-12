import sys
from typing import Optional, List, Dict
from collections import Counter

def load_data(input_path: str):
    with open(input_path, 'r') as f:
        return [line.strip() for line in f]


def parsed(line: str, pairs: Dict[str, str]) -> Optional[List[str]]:
    stack = []
    for pos, symbol in enumerate(line):
        if symbol in pairs:
            stack.append(symbol)
        else:
            open_symbol = stack.pop()
            if symbol != pairs[open_symbol]:
                return None

    return stack

def part2(input_path: str):
    data = load_data(input_path)

    pairs = {
        '(': ')',
        '{': '}',
        '[': ']',
        '<': '>',
    }

    scores = {
        ')': 1,
        ']': 2,
        '}': 3,
        '>': 4
    }

    all_totals = []
    for line in data:
        stack = parsed(line, pairs)
        if stack:
            fixup = []
            while stack:
                fixup.append(pairs[stack.pop()])

            total = 0
            for c in fixup:
                total = (total * 5) + scores[c]

            # print(f'{fixup}: {total}')
            all_totals.append(total)

    print(all_totals)
    all_totals.sort()

    middle = all_totals[len(all_totals) // 2]
    print(middle)


def part1(input_path: str):
    data = load_data(input_path)
    print(data)
    pairs = {
        '(': ')',
        '{': '}',
        '[': ']',
        '<': '>',
    }

    scores = {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137
    }

    illegal: Counter = Counter()
    for line in data:
        stack = []
        for pos, symbol in enumerate(line):
            if symbol in pairs:
                stack.append(symbol)
            else:
                open_symbol = stack.pop()
                if symbol != pairs[open_symbol]:
                    # mismatch
                    print(f'{line}: Pos: {pos}, Expected {pairs[open_symbol]}, found {symbol}')
                    illegal[symbol] += 1

    print(illegal)
    total = sum(v * scores[c] for c, v in illegal.items())
    print(total)



if __name__ == '__main__':
    part2(sys.argv[1])