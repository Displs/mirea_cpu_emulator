from loguru import logger

from domain.memory import Memory
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
        self.sf_flag = False
        self.a = Register16Bit(0)
        self.b = Register16Bit(0)
        self.c = Register16Bit(0)

    def execute(self, instruction_byte: int):
        instruction = Instruction.from_binary(instruction_byte)
        logger.info(f'Текущая команда: {instruction.command_type.name}')
        memory_value = self.get_memory_value(instruction.address_type, instruction.operand)
        self.pc.increment_by(1)
        match instruction.command_type:
            case CommandType.LDA:
                self.acc.set_value(memory_value)
                logger.info(f'В аккумулятор сохранено значение: {self.acc.value()}')
            case CommandType.STA:
                show_log = True
                if instruction.address_type == AddressingType.DIRECT:
                    self._memory.write(instruction.operand.value, self.acc.value())
                elif instruction.address_type == AddressingType.REGISTER:
                    register = self.get_register_by_type(instruction.operand)
                    register.set_value(self.acc.value())
                elif instruction.address_type == AddressingType.INDIRECT_REGISTER:
                    memory_value_address = self.get_register_by_type(instruction.operand).value()
                    self._memory.write(memory_value_address, self.acc.value())
                else:
                    show_log = False
                if show_log:
                    logger.info(f'Сохранено значение из аккумулятора: {self.acc.value()}')
            case CommandType.INC:
                if instruction.address_type == AddressingType.DIRECT:
                    memory_value_address = instruction.operand.value
                    memory_value = self._memory.read(memory_value_address)
                    self._memory.write(instruction.operand.value, memory_value + 1)
                elif instruction.address_type == AddressingType.REGISTER:
                    register = self.get_register_by_type(instruction.operand)
                    register.increment_by(1)
                elif instruction.address_type == AddressingType.INDIRECT_REGISTER:
                    memory_value_address = self.get_register_by_type(instruction.operand).value()
                    memory_value = self._memory.read(memory_value_address)
                    self._memory.write(memory_value_address, memory_value + 1)
            case CommandType.DEC:
                if instruction.address_type == AddressingType.DIRECT:
                    memory_value_address = instruction.operand.value
                    memory_value = self._memory.read(memory_value_address)
                    self._memory.write(instruction.operand.value, memory_value - 1)
                elif instruction.address_type == AddressingType.REGISTER:
                    register = self.get_register_by_type(instruction.operand)
                    register.set_value(register.value() - 1)
                elif instruction.address_type == AddressingType.INDIRECT_REGISTER:
                    memory_value_address = self.get_register_by_type(instruction.operand).value()
                    memory_value = self._memory.read(memory_value_address)
                    self._memory.write(memory_value_address, memory_value - 1)
            case CommandType.SQRT:
                self.acc.set_value(int(memory_value ** 0.5))
                logger.info(f"Результат вычисления квадратного корня: {self.acc.value()}")
            case CommandType.ADD:
                computed_sum = self.acc.value() + memory_value
                self.acc.set_value(computed_sum)
                logger.info(f"Результат сложения: {computed_sum}")
            case CommandType.SUB:
                computed_sub = self.acc.value() - memory_value
                self.acc.set_value(computed_sub)
                logger.info(f"Результат вычитания: {computed_sub}")
            case CommandType.DIV:
                computed_div = self.acc.value() // memory_value
                self.acc.set_value(computed_div)
                logger.info(f"Результат деление: {computed_div}")
            case CommandType.MUL:
                computed_mul = self.acc.value() * memory_value
                self.acc.set_value(computed_mul)
                logger.info(f"Результат умножения: {computed_mul}")
            case CommandType.CMP:
                self.z_flag = self.acc.value() == memory_value
                self.sf_flag = self.acc.value() < memory_value
                logger.info(f"Значение Z-флага: {self.z_flag}")
            case CommandType.JMP:
                self.pc.set_value(instruction.operand.value)
                logger.info(f"Переход на строку №{instruction.operand.value}")
            case CommandType.JZ:
                if self.z_flag:
                    self.pc.set_value(instruction.operand.value)
                    logger.info(f"Z-флаг равен единице. Переход на строку №{instruction.operand.value}")
                else:
                    logger.info("Z-флаг равен нулю. Переход к следующей инструкции")
            case CommandType.JNZ:
                if not self.z_flag:
                    self.pc.set_value(instruction.operand.value)
                    logger.info(f"Z-флаг равен нулю. Переход на строку №{instruction.operand.value}")
                else:
                    logger.info("Z-флаг равен единице. Переход к следующей инструкции")

            case CommandType.JL:
                if self.sf_flag:
                    self.pc.set_value(instruction.operand.value)
                    logger.info(f"SF-флаг равен единице. Переход на строку №{instruction.operand.value}")
                else:
                    logger.info("SF-флаг равен нулю. Переход к следующей инструкции")
            case CommandType.OUT:
                logger.info(f"Значение: {memory_value}")
            case CommandType.HLT:
                raise HLTException

    def execute_program(self):
        while self.pc.value() < self._memory.size:
            instruction_byte = self._memory.read(self.pc.value())
            try:
                self.execute(instruction_byte)
            except HLTException:
                break

    def get_memory_value(self, address_type: AddressingType, operand: Operand) -> int:
        match address_type:
            case AddressingType.IMMEDIATE:
                logger.info(f"Непосредственная адресация. Значение: {operand.value}")
                memory_value = operand.value
            case AddressingType.DIRECT:
                memory_value = self._memory.read(operand.value)
                logger.info(f"Прямая адресация. Адрес ячейки: {operand.value}; значение: {memory_value}")
            case AddressingType.REGISTER:
                register_type = RegisterType(operand.value)
                memory_value = self.get_register_by_type(operand).value()
                logger.info(f"Регистровая адресация. Регистр: {register_type.name}; значение: {memory_value}")
            case AddressingType.INDIRECT_REGISTER:
                register_type = RegisterType(operand.value)
                memory_value_address = self.get_register_by_type(operand).value()
                memory_value = self._memory.read(memory_value_address)
                logger.info(f"Косвенно-регистровая адресация. Регистр: {register_type.name};"
                            f" адрес ячейки: {memory_value_address};"
                            f" значение: {memory_value}")
            case _:
                raise RuntimeError(f"UNKNOWN ADDRESSING TYPE: {address_type}")
        return memory_value

    def get_register_by_type(self, operand: Operand) -> Register16Bit:
        register_type = RegisterType(operand.value)
        match register_type:
            case RegisterType.A:
                return self.a
            case RegisterType.B:
                return self.b
            case RegisterType.C:
                return self.c

    def set_start_instruction_address(self, address: int):
        self.pc.set_value(address)
