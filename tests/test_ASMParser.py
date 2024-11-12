import pprint

from domain.asm_parser import ASMParser
from schemas.addressing import AddressingType
from schemas.command import CommandType
from schemas.instruction import Instruction
from schemas.register import RegisterType


def test_parse_data_section():
    asm_parser = ASMParser()
    data_section = asm_parser.parse_data_section("num 1\nnum 2\n num 3")
    pprint.pprint(data_section)
    for index, number in enumerate([1, 2, 3]):
        assert number == data_section[index]


def test_parse_code_section():
    asm_parser = ASMParser()
    binary_instructions = asm_parser.parse_code_section("LDA ?1\nSTA /A\nADD ?0", 0)
    assert len(binary_instructions) == 3

    instruction = Instruction.from_binary(binary_instructions[0])
    assert instruction.command_type == CommandType.LDA
    assert instruction.address_type == AddressingType.DIRECT
    assert instruction.operand.value == 1

    instruction = Instruction.from_binary(binary_instructions[1])
    assert instruction.command_type == CommandType.STA
    assert instruction.address_type == AddressingType.REGISTER
    assert instruction.operand.value == RegisterType.A

    instruction = Instruction.from_binary(binary_instructions[2])
    assert instruction.command_type == CommandType.ADD
    assert instruction.address_type == AddressingType.DIRECT
    assert instruction.operand.value == 0
