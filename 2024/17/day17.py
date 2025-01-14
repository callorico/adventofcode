import sys
from typing import Tuple, Dict, List, Optional
from dataclasses import dataclass


def load_data(input_path: str) -> Tuple[Dict[str, int], List[int]]:
    with open(input_path, "rt") as f:
        # Read register values
        registers: Dict[str, int] = {}
        for line in f:
            cleaned = line.strip()
            if not cleaned:
                break

            label, value = cleaned.split(":", 1)
            _, register_name = label.split(" ", 1)
            registers[register_name.strip()] = int(value)

        _, raw_program = f.read().split(":", 1)
        program = [int(i) for i in raw_program.split(",")]

    return registers, program


@dataclass
class SideEffect:
    instruction_pointer: Optional[int] = None
    output: Optional[int] = None


def combo_operand(registers: Dict[str, int], operand: int) -> int:
    assert operand >= 0 and operand < 7, f"Received illegal combo operand value: {operand}"
    if operand <= 3:
        return operand
    elif operand == 4:
        return registers["A"]
    elif operand == 5:
        return registers["B"]
    elif operand == 6:
        return registers["C"]
    else:
        raise ValueError(f"Unexpected operand value: {operand}")


def adv(registers: Dict[str, int], operand: int) -> Optional[SideEffect]:
    denominator = pow(2, combo_operand(registers, operand))
    result = registers["A"] // denominator
    registers["A"] = result


def bxl(registers: Dict[str, int], operand: int) -> Optional[SideEffect]:
    result = registers["B"] ^ operand
    registers["B"] = result


def bst(registers: Dict[str, int], operand: int) -> Optional[SideEffect]:
    registers["B"] = combo_operand(registers, operand) % 8


def jnz(registers: Dict[str, int], operand: int) -> Optional[SideEffect]:
    if registers["A"] != 0:
        return SideEffect(instruction_pointer=operand)


def bxc(registers: Dict[str, int], operand: int) -> Optional[SideEffect]:
    registers["B"] = registers["B"] ^ registers["C"]


def out(registers: Dict[str, int], operand: int) -> Optional[SideEffect]:
    result = combo_operand(registers, operand) % 8
    return SideEffect(output=result)


def bdv(registers: Dict[str, int], operand: int) -> Optional[SideEffect]:
    denominator = pow(2, combo_operand(registers, operand))
    result = registers["A"] // denominator
    registers["B"] = result


def cdv(registers: Dict[str, int], operand: int) -> Optional[SideEffect]:
    denominator = pow(2, combo_operand(registers, operand))
    result = registers["A"] // denominator
    registers["C"] = result


OPCODES = {
    0: adv,
    1: bxl,
    2: bst,
    3: jnz,
    4: bxc,
    5: out,
    6: bdv,
    7: cdv,
}


def run_program(registers: Dict[str, int], program: List[int]) -> List[int]:
    i = 0
    outputs = []
    while i < len(program):
        opcode = program[i]
        operand = program[i+1]

        fn = OPCODES[opcode]
        #print(f"{fn.__name__} {operand} {registers}")
        result: SideEffect = fn(registers, operand) or SideEffect()
        if result.output is not None:
            outputs.append(result.output)
        #print(f"  -> {result} {registers}")

        if result.instruction_pointer is not None:
            i = result.instruction_pointer
        else:
            i += 2

    return outputs


def main(input_path: str):
    registers, program = load_data(input_path)
    assert len(program) % 2 == 0, "Badly formatted program. op is missing an operand"

    print(f"Target program: {program}. Length: {len(program)}")

    # Through observation, a new digit is added to the output every power of 8
    # 8: 2 digits
    # 64: 3 digits
    # 512 4 digits
    #
    # Also through observation, it appears that digits in index position i change
    # once every pow(8, i) increments of A

    # This is the smallest value of a that will produce a program output of the
    # desired length
    a = pow(8, len(program) - 1)
    start = a
    while True:
        index = len(program) - 1
        registers["A"] = a
        registers["B"] = 0
        registers["C"] = 0
        outputs = run_program(registers, program)
        print(f"offset: {a - start}, a: {a} -> {outputs}")
        assert len(outputs) == len(program)
        if outputs == program:
            break

        # Find the biggest index that does not currently match and increment
        # by the smallest value that will cause it to update
        while outputs[index] == program[index]:
            index -= 1
        assert index >= 0

        increment = pow(8, index)

        a += increment

    print(a)

    # print(registers)
    # print(program)
    # outputs = run_program(registers, program)
    # program_output = ",".join(str(v) for v in outputs)
    # print(program_output)
    # print(registers)



if __name__ == "__main__":
    main(sys.argv[1])