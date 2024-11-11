from domain.memory import MemoryCell

WasOverflow = bool


class Register16Bit:
    def __init__(self, value: int):
        self._memory_cell = MemoryCell(value)

    def increment_by(self, value: int) -> WasOverflow:
        result = self._memory_cell.read() + value
        self._memory_cell.write(result)
        return result > self._memory_cell.read()

    def set_value(self, value: int):
        self._memory_cell.write(value)

    def value(self) -> MemoryCell:
        return self._memory_cell