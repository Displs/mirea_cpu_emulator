from schemas.addressing import AddressingType
from schemas.command import CommandType
from schemas.instruction import Instruction


def test_from_text():
    instruction = Instruction.from_text("LDA /30")

    assert instruction.command_type == CommandType.LDA
    assert instruction.address_type == AddressingType.REGISTER
    assert instruction.operand == 30


def test_from_binary():
    instruction = Instruction.from_text("LDA /30")

    binary_instruction = instruction.as_binary()
    decoded_instruction = instruction.from_binary(binary_instruction)

    assert instruction.command_type == decoded_instruction.command_type
    assert instruction.address_type == decoded_instruction.address_type
    assert instruction.operand == decoded_instruction.operand
