import sys
import re


def load_data(input_path: str) -> str:
    with open(input_path, 'rt') as f:
        return f.read()


def main(input_path):
    program = load_data(input_path)

    # Part 1
    # matches = re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", program)
    # total = sum(int(m[0]) * int(m[1]) for m in matches)
    # print(total)

    # Part 2
    matches = re.findall(r"(don't\(\)|mul\((\d{1,3}),(\d{1,3})\)|do\(\))", program)
    mul_enabled = True
    total = 0
    for m in matches:
        if m[0] == "don't()":
            mul_enabled = False
        elif m[0] == "do()":
            mul_enabled = True
        else:
            if mul_enabled:
                total += int(m[1]) * int(m[2])

    print(total)


if __name__ == '__main__':
    main(sys.argv[1])


