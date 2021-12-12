import sys
from typing import List, Optional

def load_data(input_path: str) -> List[int]:
    with open(input_path, 'r') as f:
        return [int(n) for n in f.readline().split(',')]

def part1(crabs: List[int]) -> int:
    min_fuel: Optional[int] = None
    for candidate in crabs:
        fuel = 0
        for c in crabs:
            fuel += int(abs(candidate - c))

        if min_fuel is None or fuel < min_fuel:
            min_fuel = fuel
            print(f'Crab {candidate} best so far at {min_fuel}')

    assert min_fuel is not None
    return min_fuel

def fuel_cost(target_pos: int, crab: int, cached: List[int]):
    distance = int(abs(target_pos - crab))
    return cached[distance]

def part2(crabs: List[int]) -> int:
    print(len(crabs))

    min_crab = min(crabs)
    max_crab = max(crabs)

    sum = 0
    cached = [0]
    for i in range(max_crab):
        sum += (i + 1)
        cached.append(sum)

    print(min_crab, max_crab, cached)

    min_fuel: Optional[int] = None
    for candidate in range(min_crab, max_crab + 1):
        fuel = 0
        for c in crabs:
            fuel += fuel_cost(candidate, c, cached)

        if min_fuel is None or fuel < min_fuel:
            min_fuel = fuel
            print(f'{candidate} best target so far at {min_fuel}')

    assert min_fuel is not None
    return min_fuel


def main(input_path: str):
    data = load_data(input_path)
    print(data)
    fuel = part2(data)

    print(fuel)

if __name__ == '__main__':
    main(sys.argv[1])