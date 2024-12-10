import sys
from typing import List
from collections import deque


class File:
    def __init__(self, file_id, size, space_after):
        self.file_id = file_id
        self.size = size
        self.space_after = space_after


def load_data(input_path: str) -> List[File]:
    disk_layout = []
    with open(input_path, 'rt') as f:
        raw_disk = f.read().strip()
        # Tack on an empty space after to make the ensuing parsing easier
        if len(raw_disk) % 2 != 0:
            raw_disk += "0"

        file_id = 0
        for i in range(0, len(raw_disk) - 1, 2):
            file_size = int(raw_disk[i])
            space_after = int(raw_disk[i+1])
            disk_layout.append(File(file_id, file_size, space_after))
            file_id += 1

    return disk_layout


def part1(disk_layout):
    total_size = sum(f.size for f in disk_layout)

    disk = []
    curr = 0
    last = len(disk_layout) - 1
    last_file = disk_layout[last]
    last_file_remaining = last_file.size

    while curr < last:
        curr_file = disk_layout[curr]
        disk.extend([curr_file.file_id] * curr_file.size)

        # Fill space after the current file with the last file
        space_to_fill = curr_file.space_after
        while space_to_fill > 0:
            chunk = min(space_to_fill, last_file_remaining)
            disk.extend([last_file.file_id] * chunk)
            last_file_remaining -= chunk
            space_to_fill -= chunk
            assert last_file_remaining >= 0 and space_to_fill >= 0
            if not last_file_remaining:
                if last <= curr + 1:
                    # Cannot backfill from the end anymore
                    break

                last -= 1
                last_file = disk_layout[last]
                last_file_remaining = last_file.size

        # Advance to the next file
        curr += 1

    # Append on the final chunk
    disk.extend([last_file.file_id] * last_file_remaining)

    print(f"compacted disk: {len(disk)}, expected: {total_size}")
    checksum = sum(i * file_id for i, file_id in enumerate(disk))
    print(checksum)

def main(input_path):
    disk_layout = load_data(input_path)

    part1(disk_layout)


if __name__ == '__main__':
    main(sys.argv[1])

