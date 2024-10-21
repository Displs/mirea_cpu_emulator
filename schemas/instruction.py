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

