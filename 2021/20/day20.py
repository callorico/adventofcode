import sys
from typing import List, Tuple

def load_data(input_path: str) -> Tuple[str, List[str]]:
    with open(input_path, 'r') as f:
        enhancement = f.readline().strip()
        assert len(enhancement) == 512

        f.readline()

        image = [line.strip() for line in f]
        return enhancement, image

def mask(image: List[str], row: int, col: int, default: str) -> int:
    rows = len(image)
    cols = len(image[0])

    mask: List[str] = []
    for r_delta in [-1, 0, 1]:
        for c_delta in [-1, 0, 1]:
            new_row = row + r_delta
            new_col = col + c_delta

            if new_row < 0 or new_row >= rows or new_col < 0 or new_col >= cols:
                mask.append(default)
                continue

            if image[new_row][new_col] == '.':
                mask.append('0')
            else:
                mask.append('1')

    return int(''.join(mask), 2)


def print_image(image: List[str]):
    for r in image:
        print(r)


def enhance(enhancement: str, image: List[str], rounds: int) -> List[str]:
    rows = len(image)
    cols = len(image[0])
    print(f'r: {rows}, c: {cols}')
    print_image(image)

    default = '0'

    border = 3
    for round in range(rounds):
        output_image = []
        for r in range(-border, rows + border):
            output_image.append(
                ''.join(
                    enhancement[mask(image, r, c, default)]
                    for c in range(-border, cols + border)
                )
            )

        image = output_image
        print(f'After round {round + 1}')
        print_image(image)
        rows = len(image)
        cols = len(image[0])

        default = '0' if enhancement[int(default * 9, 2)] == '.' else '1'

    return image


def pixel_count(image: List[str]) -> int:
    total_set = 0
    for r in image:
        total_set += sum(1 for c in r if c == '#')

    return total_set


def part1(input_path: str):
    enhancement, image = load_data(input_path)
    enhanced = enhance(enhancement, image, 2)
    total_set = pixel_count(enhanced)
    print(f'Total pixels set: {total_set}')


def part2(input_path: str):
    enhancement, image = load_data(input_path)
    enhanced = enhance(enhancement, image, 50)
    total_set = pixel_count(enhanced)
    print(f'Total pixels set: {total_set}')


if __name__ == '__main__':
    part2(sys.argv[1])