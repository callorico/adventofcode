import sys
from typing import Optional


class SparseMap:
    def __init__(self, ranges: list[list[int]], label: str):
        self.ranges = sorted(ranges, key=lambda k: k[1])
        self.label = label.strip()

    def __getitem__(self, val: int) -> int:
        for range in self.ranges:
            if val >= range[1] and val < range[1] + range[2]:
                return range[0] + val - range[1]

        return val

    def __repr__(self):
        return f"{self.label} -> {self.ranges}"


def parse_numbers(number_text: str) -> list[int]:
    return [int(n) for n in number_text.split(" ") if n]


def parse_map(f, label: str) -> SparseMap:
    ranges: list[list[int]] = []
    while True:
        line = f.readline().strip()
        if not line:
            return SparseMap(ranges, label)

        ranges.append(parse_numbers(line))


def load_data(input_path):
    with open(input_path, "r") as f:
        seeds_text = f.readline()
        seeds: list[int] = parse_numbers(seeds_text.split(": ", 1)[1])
        print(seeds)

        f.readline()
        mappings = []
        while True:
            label = f.readline()
            if not label:
                break
            mappings.append(parse_map(f, label))

    print(mappings)

    curr_min: Optional[int] = None
    for s in seeds:
        print(f"Evaluating seed {s}")
        v = s
        for mapping in mappings:
            # print(f"{mapping.label}: {v} -> {mapping[v]}")
            v = mapping[v]

        print(f"seed {s} mapped to {v}")
        
        if not curr_min or v < curr_min:
            curr_min = v

    print(curr_min)


def main(input_path):
    load_data(input_path)

if __name__ == "__main__":
    main(sys.argv[1])