from schemas.addressing import AddressingType
from schemas.command import CommandType
from schemas.operand import Operand


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
        return Instruction(CommandType.from_name(command_name),
                           AddressingType.from_name(addressing_name),
                           Operand.from_text(operand_text))

    def as_binary(self, ) -> int:
        return (self.command_type.value << 12) | (self.address_type.value << 10) | (self.operand.value & 1023)

    @staticmethod
    def from_binary(binary: int):
        command_type = (binary >> 12) & 15
        address_type = (binary >> 10) & 3
        operand = (binary & 1023)
        return Instruction(CommandType(command_type),
                           AddressingType(address_type),
                           Operand(operand))
