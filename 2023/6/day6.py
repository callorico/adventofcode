import sys
from typing import Tuple


def parse_numbers(number_text: str) -> list[int]:
    return [int(n) for n in number_text.split(" ") if n]

def parse_numbers2(number_text: str) -> int:
    return int(number_text.replace(" ", ""))


def load_data(input_path) -> Tuple[int, int]:
    with open(input_path, "r") as f:
        time_line = f.readline()
        _, numbers = time_line.split(":", 2)
        time = parse_numbers2(numbers)

        distance_line = f.readline()
        _, numbers = distance_line.split(":", 2)
        distance = parse_numbers2(numbers)
        return time, distance


def num_possible_wins(duration: int, distance: int) -> int:
    wins = 0
    
    for hold_duration in range(duration + 1):
        time_remaining = duration - hold_duration
        distance_travelled = time_remaining * hold_duration
        # print(f"hold: {hold_duration} -> {distance_travelled}")
        if distance_travelled > distance:
            wins += 1

    return wins


def main(input_path):
    time, distance = load_data(input_path)
    print(time)
    print(distance)

    possible_wins = num_possible_wins(time, distance)
    print(f"Total ways to win: {possible_wins}")
    # assert len(times) == len(distances)
    # num_races = len(times)

    # combinations = 1
    # for i in range(num_races):
    #     ways_to_win = num_possible_wins(times[i], distances[i])
    #     print(f"# ways to win race {i} (duration: {times[i]}, distance: {distances[i]}): {ways_to_win}")
    #     combinations *= ways_to_win

    # print(f"Total ways to win: {combinations}")


if __name__ == "__main__":
    main(sys.argv[1])