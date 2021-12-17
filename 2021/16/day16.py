import sys
from typing import List, Tuple

def load_data(input_path: str) -> str:
    with open(input_path, 'r') as f:
        contents = f.read().strip()
        return ''.join(bin(int(c, 16))[2:].zfill(4) for c in contents)


def chunk(packet: str, start: int, end: int) -> int:
    raw = packet[start:end]
    print(raw)
    return int(packet[start:end], 2)


def parse_packet2(packet: str, offset: int) -> Tuple[int, int]:
    version = chunk(packet, offset, offset + 3)
    offset += 3

    message_type = chunk(packet, offset, offset + 3)
    offset += 3

    print(f'version: {version}, message type: {message_type}')
    if message_type == 4:
        # Literal
        binary_segments = []
        while True:
            segment = packet[offset:offset + 5]
            offset += 5
            binary_segments.append(segment[1:])
            if segment[0] == '0':
                break

        value = int(''.join(binary_segments), 2)
    else:
        # Operator
        values = []
        length_type = packet[offset:offset + 1]
        offset += 1
        if length_type == '0':
            length = chunk(packet, offset, offset + 15)
            offset += 15
            end = offset + length
            while offset < end:
                sub_value, offset = parse_packet2(packet, offset)
                values.append(sub_value)
        elif length_type == '1':
            num_packets = chunk(packet, offset, offset + 11)
            offset += 11
            for _ in range(num_packets):
                sub_value, offset = parse_packet2(packet, offset)
                values.append(sub_value)
        else:
            assert False, 'Should never get here'

        if message_type == 0:
            return sum(values), offset
        elif message_type == 1:
            product = values[0]
            for v in values[1:]:
                product *= v
            return product, offset
        elif message_type == 2:
            return min(values), offset
        elif message_type == 3:
            return max(values), offset
        elif message_type == 5:
            assert len(values) == 2
            return int(values[0] > values[1]), offset
        elif message_type == 6:
            assert len(values) == 2
            return int(values[0] < values[1]), offset
        elif message_type == 7:
            assert len(values) == 2
            return int(values[0] == values[1]), offset

    print(f'Returning value: {value}')
    return value, offset

def parse_packet(packet: str, offset: int, versions: List[int]) -> int:
    version = chunk(packet, offset, offset + 3)
    versions.append(version)
    offset += 3

    message_type = chunk(packet, offset, offset + 3)
    offset += 3

    print(f'version: {version}, message type: {message_type}')
    if message_type == 4:
        # Literal
        binary_segments = []
        while True:
            segment = packet[offset:offset + 5]
            offset += 5
            binary_segments.append(segment[1:])
            if segment[0] == '0':
                break

        value = int(''.join(binary_segments), 2)
        # TODO: Need to normalize the offset to the hex boundary?
        print(f'Literal value: {value}')
    else:
        # Operator
        length_type = packet[offset:offset + 1]
        offset += 1
        if length_type == '0':
            length = chunk(packet, offset, offset + 15)
            offset += 15
            end = offset + length
            while offset < end:
                offset = parse_packet(packet, offset, versions)
        elif length_type == '1':
            num_packets = chunk(packet, offset, offset + 11)
            offset += 11
            for _ in range(num_packets):
                offset = parse_packet(packet, offset, versions)
        else:
            assert False, 'Should never get here'

    return offset


def part1(input_path: str):
    packet = load_data(input_path)
    versions: List[int] = []
    parse_packet(packet, 0, versions)
    v_sum = sum(versions)
    print(f'Version sum: {v_sum}')


def part2(input_path: str):
    packet = load_data(input_path)
    value, offset = parse_packet2(packet, 0)
    print(f'Calculated value: {value}')

if __name__ == '__main__':
    part2(sys.argv[1])