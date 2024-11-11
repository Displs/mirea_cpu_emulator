from enum import Enum


class AddressingType(int, Enum):
    """ Тип адресации (2 бита) """
    DIRECT = 0             # Прямая адресация (?); LDA ?30 - Загрузить в аккумулятор слово из ячейки с адресом 30
    IMMEDIATE = 1          # Непосредственная адресация (#); LDA #30 - загрузить в аккумулятор слово "30", в команде содержится сам операнд, загрузка его из памяти не требуется
    REGISTER = 2           # Регистровая адресация (/); LDA /A - Загрузить в аккумулятор слово из регистра A
    INDIRECT_REGISTER = 3  # Косвенно-регистровая адресация (@); LDA @30 - загрузить в аккумулятор слово из ячейки, адрес которой находится в ячейке 30, в команде содержится адрес адреса операнд

    @staticmethod
    def from_name(name: str):
        try:
            addressing_type = addressing_type_by_name[name]
        except KeyError:
            raise ValueError(f"Unknown addressing type: {name}")
        else:
            return addressing_type


addressing_type_by_name = {
    '?': AddressingType.DIRECT,
    '#': AddressingType.IMMEDIATE,
    '/': AddressingType.REGISTER,
    '@': AddressingType.INDIRECT_REGISTER
}
