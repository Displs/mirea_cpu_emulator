from schemas.addressing import AddressingType
from schemas.command import CommandType
from schemas.operand import Operand
from schemas.register import RegisterType


class Instruction:

    def __init__(self,
                 command_type: CommandType,
                 address_type: AddressingType,
                 operand: Operand):
        self.command_type = command_type
        self.address_type = address_type
        self.operand = operand

    @staticmethod
    def from_text(text: str) -> 'Instruction':
        command_name, addressing_name_and_operand_text = text.split(' ')
        addressing_name = addressing_name_and_operand_text[0]
        operand_text = addressing_name_and_operand_text[1:]
        try:
            operand = Operand.from_text(operand_text)
        except ValueError:
            operand = Operand(RegisterType.from_name(operand_text))
        return Instruction(CommandType.from_name(command_name),
                           AddressingType.from_name(addressing_name),
                           operand)

    def as_binary(self, ) -> int:
        sign_bit = 1 if self.operand.value < 0 else 0
        operand_value = abs(self.operand.value)
        return (self.command_type.value << 12) | (self.address_type.value << 10) | (sign_bit << 9) | (operand_value & 511)

    @staticmethod
    def from_binary(binary: int):
        command_type = (binary >> 12) & 15
        address_type = (binary >> 10) & 3
        sign = -1 if ((binary >> 9) & 1) == 1 else 1
        operand = (binary & 511)
        return Instruction(CommandType(command_type),
                           AddressingType(address_type),
                           Operand(sign * operand))

    def __repr__(self):
        return f"Instruction(command_type={self.command_type.name}," \
               f" addressing_type={self.address_type.name}," \
               f" operand={self.operand.value})"