import sys
from typing import Dict

def load_data(input_path: str):
    with open(input_path, 'r') as f:
        return [l for l in f.read().splitlines() if l.strip()]


def main(input_path):
    data = load_data(input_path)
    total = 0
    for line in data:
        first_digit = None
        last_digit = None
        for c in line:
            try:
                converted = int(c)
                if first_digit is None:
                    first_digit = converted
                else:
                    last_digit = converted
            except ValueError:
                pass

        if last_digit is None:
            last_digit = first_digit

        total += int(f"{first_digit}{last_digit}") 

    print(total)

if __name__ == '__main__':
    main(sys.argv[1])