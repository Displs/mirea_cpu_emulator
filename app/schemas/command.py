import enum


class CommandType(int, enum.Enum):
    """ Тип команды (4 бита). CPU, используя инструкцию, выполняет действие над памятью """

    LDA = 0   # Загрузка данных в аккумулятор с переданного типа адресации по конкретному адресу
    STA = 1   # Сохранение данных аккумулятора в память по переданному типу адресации
    ADD = 2   # Сложение
    INC = 3   # Увеличение значения ячейки памяти на 1
    JZ = 4    # Условный переход
    CMP = 5   # Сравнение
    SUB = 6  # Вычитание
    JMP = 7  # Безусловный переход
    HLT = 15  # Выход

    @staticmethod
    def from_name(name: str) -> 'CommandType':
        for command_type in CommandType:
            if command_type.name == name:
                return command_type
        raise ValueError(f'Unknown command name: {name}')
