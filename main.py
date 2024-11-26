from pathlib import Path

from domain.asm_parser import ASMParser
from domain.cpu import CPU
from domain.memory import Memory


def main():
    asm_parser = ASMParser()
    memory = Memory(256)
    program_text = Path('array_sum.asm').read_text('utf-8')
    start_instruction_address = asm_parser.load_program_to_memory(program_text,
                                                                  memory)
    cpu = CPU(memory)
    cpu.set_start_instruction_address(start_instruction_address)
    cpu.execute_program()


if __name__ == '__main__':
    main()
