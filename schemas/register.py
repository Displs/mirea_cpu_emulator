from enum import Enum


class RegisterType(int, Enum):
    A = 0
    B = 1
    C = 2
    D = 3

    AC = 4
    PC = 5
    IR = 6

    FLAGS = 7

    @staticmethod
    def from_name(name: str) -> 'RegisterType':
        for register_type in RegisterType:
            if register_type.name == name:
                return register_type
        raise ValueError(f'Unknown register name: {name}')
