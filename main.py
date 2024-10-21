import enum


class RegisterName(str, enum.Enum):
    EAX = "eax"
    EBX = "ebx"
    ECX = "ecx"
    EDX = "edx"
    ESP = "esp"
    EBP = "ebp"
    ESI = "esi"
    EDI = "edi"
    EIP = "eip"
    EFLAGS = "eflags"


def main():
    pass


if __name__ == '__main__':
    main()
