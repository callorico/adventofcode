import sys
from typing import Iterable


def parse_number(number_text: str) -> list[int]:
    return [int(n) for n in number_text.split(" ") if n]


def load_data(input_path) -> Iterable[list[int]]:
    with open(input_path, "r") as f:
        for line in f:
            yield parse_number(line.strip())


def next_value(history: list[int]) -> int:
    print(history)
    if all(n == 0 for n in history):
        return 0
    
    reduced = [history[n]-history[n-1] for n in range(1, len(history))]
    return history[0] - next_value(reduced)


def main(input_path):
    values = 0
    for history in load_data(input_path):
        values += next_value(history)

    print(f"Extrapolated value sum {values}")
        


if __name__ == "__main__":
    main(sys.argv[1])