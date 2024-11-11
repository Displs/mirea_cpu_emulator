from abc import abstractmethod


class MemoryCellI:

    @abstractmethod
    def read(self) -> int:
        pass

    @abstractmethod
    def write(self, value: int):
        pass


class MemoryCell(MemoryCellI):

    def __init__(self, value: int):
        self._value = value & 65_535

    def read(self) -> int:
        return self._value

    def write(self, value: int):
        self._value = value & 65_535


class Memory:

    def __init__(self, size: int):
        self._size = size
        self._storage = [MemoryCell(0) for _ in range(size)]

    @property
    def size(self):
        return self._size

    def read(self, address: int) -> MemoryCell:
        return self._storage[address]

    def write(self, address: int, value: int):
        if address >= self._size:
            raise RuntimeError(f"Attempt to write data to does not existing address={address}")
        self._storage[address].write(value)
