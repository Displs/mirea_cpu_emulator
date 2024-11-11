from schemas.addressing import AddressingType
from schemas.command import CommandType
from schemas.instruction import Instruction
from schemas.operand import Operand
from schemas.register import RegisterType


def test_command_lda(cpu, memory):
    # immediate
    instruction = Instruction(CommandType.LDA,
                              AddressingType.IMMEDIATE,
                              Operand(10))
    cpu.execute(instruction.as_binary())
    assert cpu.acc.value().read() == instruction.operand.value

    # direct
    address = 1
    value = 15
    memory.write(address, value)
    instruction = Instruction(CommandType.LDA,
                              AddressingType.DIRECT,
                              Operand(address))
    cpu.execute(instruction.as_binary())
    assert cpu.acc.value().read() == value

    # register
    register_type = RegisterType.A
    cpu.a.set_value(155)
    instruction = Instruction(CommandType.LDA,
                              AddressingType.REGISTER,
                              Operand(register_type.value))
    cpu.execute(instruction.as_binary())
    assert cpu.acc.value().read() == cpu.a.value().read()

    # indirect-register
    register_type = RegisterType.B
    address = 50
    value = 7000
    memory.write(address, value)
    cpu.b.set_value(address)
    instruction = Instruction(CommandType.LDA,
                              AddressingType.INDIRECT_REGISTER,
                              Operand(register_type.value))
    cpu.execute(instruction.as_binary())
    assert cpu.acc.value().read() == value
