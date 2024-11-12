
WasOverflow = bool


class Register16Bit:
    def __init__(self, value: int):
        self._value = value

    def increment_by(self, value: int) -> WasOverflow:
        result = self._value + value
        self._value = result
        return result > self._value

    def set_value(self, value: int):
        self._value = value

    def value(self) -> int:
        return self._value
