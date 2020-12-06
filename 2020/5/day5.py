import sys

def load_data(input_path):
    with open(input_path, 'r') as f:
        return [l.strip() for l in f.readlines()]


def binary_search(sequence, min, max, smaller, bigger):
    print(sequence)
    result = None
    for i in range(len(sequence)):
        midpoint = min + ((max - min) // 2)
        if sequence[i] == smaller:
            max = midpoint
            result = max - 1
        elif sequence[i] == bigger:
            min = midpoint
            result = min
        else:
            raise ValueError(f'Unknown {sequence}, {sequence[i]}')

        #print(f'min: {min}, max: {max}, result: {result}')

    return result

def get_seat_number(seat):
    #print(seat)

    row = binary_search(seat[:7], 0, 128, 'F', 'B')
    col = binary_search(seat[7:], 0, 8, 'L', 'R')

    seat_id = row * 8 + col
    #print(f'row {row}, col {col}, seat_id: {seat_id}')

    return seat_id


def main(input_path):
    all_seats = set()
    for row in range(128):
        for col in range(8):
            all_seats.add(row * 8 + col)

    seats = load_data(input_path)
    for s in seats:
        all_seats.remove(get_seat_number(s))
    #max_seat_id = max(get_seat_number(s) for s in seats)

    for id in sorted(all_seats):
        print(id)

if __name__ == '__main__':
    main(sys.argv[1])
