import sys
import re
from typing import List, Tuple, Iterable
from itertools import product
import math


def load_data(input_path: str) -> List[Tuple[int, List[int]]]:
    equations = []
    with open(input_path, 'rt') as f:
        for line in f:
            cleaned = line.strip()
            if not cleaned:
                break

            raw_sum, raw_operands = cleaned.split(": ", 1)
            operands = [int(o) for o in raw_operands.split(" ")]
            equations.append((int(raw_sum), operands))
    return equations


def main(input_path):
    equations = load_data(input_path)

    result = 0
    for sum, operands in equations:
        print(sum, operands)
        operator_combos = product("+*", repeat=len(operands) - 1)

        for ops in operator_combos:
            total = operands[0]
            for op, operand in zip(ops, operands[1:]):
                if op == "*":
                    total *= operand
                elif op == "+":
                    total += operand
                else:
                    raise Exception(f"Unknown operator {op}")

            # print(f"{ops} {operands} -> {total}. Expected: {sum}")
            if total == sum:
                result += total
                break

    print(result)





if __name__ == '__main__':
    main(sys.argv[1])
