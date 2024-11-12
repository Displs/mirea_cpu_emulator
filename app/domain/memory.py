class Memory:

    def __init__(self, size: int):
        self._size = size
        self._storage = [0] * size

    @property
    def size(self):
        return self._size

    def read(self, address: int) -> int:
        return self._storage[address]

    def write(self, address: int, value: int):
        if address >= self._size:
            raise RuntimeError(f"Attempt to write data to does not existing address={address}")
        self._storage[address] = value
