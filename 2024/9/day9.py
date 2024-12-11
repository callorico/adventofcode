import sys
from typing import List, Optional
from dataclasses import dataclass


class File:
    def __init__(self, file_id, size, space_after):
        self.file_id = file_id
        self.size = size
        self.space_after = space_after


@dataclass
class Span:
    index: int
    file_id: Optional[int]
    length: int

    def score(self) -> int:
        if not self.file_id:
            return 0

        return sum((self.index + i) * self.file_id for i in range(self.length))


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


def print_disk(disk: List[Span]):
    prev_span = None
    for span in disk:
        if prev_span:
            gap_size = span.index - (prev_span.index + prev_span.length)
            print("." * gap_size, end=" ")
        print(str(span.file_id) * span.length, end=" ")
        prev_span = span
    print()


def main(input_path):
    disk_layout = load_data(input_path)
    #part1(disk_layout)

    # Part 2
    disk: List[Span] = []
    index = 0
    for f in disk_layout:
        disk.append(Span(index, f.file_id, f.size))
        index += f.size
        if f.space_after:
            index += f.space_after

    curr_file_id = disk[-1].file_id
    #print_disk(disk)

    while curr_file_id >= 0:
        # Find file with specified ID
        curr_file_index = -1
        for i in range(len(disk)):
            if disk[i].file_id == curr_file_id:
                curr_file_index = i
                break

        # Find gap between two adjacent files that curr_file can
        # be inserted into
        for i in range(curr_file_index):
            if i+1 < len(disk):
                this_span = disk[i]
                next_span = disk[i+1]
                free_space = next_span.index - (this_span.index + this_span.length)
                if disk[curr_file_index].length <= free_space:
                    # Insert into gap
                    curr_file = disk[curr_file_index]
                    del disk[curr_file_index]
                    curr_file.index = this_span.index + this_span.length
                    disk.insert(i+1, curr_file)
                    break

        #print_disk(disk)
        curr_file_id -= 1

    total = sum(span.score() for span in disk)
    print(total)



if __name__ == '__main__':
    main(sys.argv[1])

