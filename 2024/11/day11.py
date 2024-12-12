import sys
from typing import List


def load_data(input_path) -> List[int]:
    with open(input_path, "rt") as f:
        return [int(s) for s in f.read().strip().split(" ")]


def main(input_path):
    stones = load_data(input_path)
    print(stones)

    for round in range(25):
        #print(f"{round}: {stones}")
        new_stones = []
        for s in stones:
            # apply rules in order
            if s == 0:
                new_stones.append(1)
                continue

            converted = str(s)
            if len(converted) % 2 == 0:
                mid = len(converted) // 2
                new_stones.append(int(converted[:mid]))
                new_stones.append(int(converted[mid:]))
                continue

            new_stones.append(s * 2024)

        stones = new_stones

    print(len(stones))


if __name__ == "__main__":
    main(sys.argv[1])
