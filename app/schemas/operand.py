

class Operand:
    """ Адрес операнда в памяти (10 бит) """

    def __init__(self, value: int):
        self.value = value

    @staticmethod
    def from_text(text: str):
        return int(text)