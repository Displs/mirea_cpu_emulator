from typing import List

from loguru import logger

from domain.memory import Memory, MemoryCell
from domain.registers.register_16 import Register16Bit
from schemas.addressing import AddressingType
from schemas.command import CommandType
from schemas.exceptions import HLTException
from schemas.instruction import Instruction
from schemas.operand import Operand
from schemas.register import RegisterType


class CPU:

    def __init__(self, memory: Memory):
        self._memory = memory

        self.pc = Register16Bit(0)
        self.acc = Register16Bit(0)
        self.flags = Register16Bit(0)

        self.z_flag = False
        self.a = Register16Bit(0)
        self.b = Register16Bit(0)
        self.c = Register16Bit(0)

    def execute(self, instruction_byte: int):
        instruction = Instruction.from_binary(instruction_byte)
        logger.info(f'Текущая команда: {instruction.command_type.name}')
        cell = self.get_memory_cell(instruction.address_type, instruction.operand)
        self.pc.increment_by(1)
        match instruction.command_type:
            case CommandType.LDA:
                self.acc.set_value(cell.read())
            case CommandType.STA:
                cell.write(self.acc.value().read())
            case CommandType.ADD:
                computed_sum = self.acc.value().read() + cell.read()
                self.acc.set_value(computed_sum)
            case CommandType.SUB:
                computed_sub = self.acc.value().read() - cell.read()
                self.acc.set_value(computed_sub)
            case CommandType.CMP:
                self.z_flag = self.acc.value().read() == cell.read()
            case CommandType.JMP:
                self.pc.set_value(instruction.operand.value)
            case CommandType.JZ:
                if not self.z_flag:
                    self.pc.set_value(instruction.operand.value)
            case CommandType.INC:
                cell.write(cell.read() + 1)
            case CommandType.HLT:
                raise HLTException

    def execute_program(self):
        while self.pc.value().read() < self._memory.size:
            instruction_byte = self._memory.read(self.pc.value().read()).read()
            try:
                self.execute(instruction_byte)
            except HLTException:
                break

    def get_memory_cell(self, address_type: AddressingType, operand: Operand) -> MemoryCell:
        match address_type:
            case AddressingType.IMMEDIATE:
                logger.info(f"Непосредственная адресация. Значение: {operand.value}")
                memory_cell = MemoryCell(operand.value)
            case AddressingType.DIRECT:
                memory_cell = self._memory.read(operand.value)
                logger.info(f"Прямая адресация. Адрес ячейки: {operand.value}; значение: {memory_cell.read()}")
            case AddressingType.REGISTER:
                register_type = RegisterType(operand.value)
                memory_cell = self.get_register_as_memory_cell(operand)
                logger.info(f"Регистровая адресация. Регистр: {register_type.name}; значение: {memory_cell.read()}")
            case AddressingType.INDIRECT_REGISTER:
                register_type = RegisterType(operand.value)
                register = self.get_register_as_memory_cell(operand)
                memory_cell_address = register.read()
                memory_cell = self._memory.read(memory_cell_address)
                logger.info(f"Косвенно-регистровая адресация. Регистр: {register_type.name};"
                            f" адрес ячейки: {memory_cell_address};"
                            f" значение: {memory_cell.read()}")
            case _:
                raise RuntimeError(f"UNKNOWN ADDRESSING TYPE: {address_type}")
        return memory_cell

    def get_register_as_memory_cell(self, operand: Operand) -> MemoryCell:
        register_type = RegisterType(operand.value)
        match register_type:
            case RegisterType.A:
                return self.a.value()
            case RegisterType.B:
                return self.b.value()
            case RegisterType.C:
                return self.c.value()

    def set_start_instruction_address(self, address: int):
        self.pc.set_value(address)
