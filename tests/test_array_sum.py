from schemas.addressing import AddressingType
from schemas.command import CommandType
from schemas.instruction import Instruction
from schemas.operand import Operand
from schemas.register import RegisterType


def test_sum(cpu, memory):
    arr = [10, 4, 7, 5, 3]
    arr_size = len(arr)
    element_address = 1
    memory.write(0, arr_size)
    for arr_element in arr:
        memory.write(element_address, arr_element)
        element_address += 1

    start_instruction_address = element_address + 1
    instructions = [
        Instruction(CommandType.LDA, AddressingType.IMMEDIATE, Operand(1)),  #  Загрузить адрес первого элемента в аккумулятор
        Instruction(CommandType.STA, AddressingType.REGISTER, Operand(RegisterType.A)),  # Загрузить в регистр A адрес первого элемента
        Instruction(CommandType.ADD, AddressingType.DIRECT, Operand(0)),  # Получить в аккумуляторе адрес ячейки памяти после последнего элемента массива
        Instruction(CommandType.STA, AddressingType.REGISTER, Operand(RegisterType.B)),  # Загрузить адрес ячейки памяти после последнего элемента массива в регистр B
        Instruction(CommandType.LDA, AddressingType.IMMEDIATE, Operand(0)),  # Очистить значение аккумулятора
        # Начало цикла
        Instruction(CommandType.ADD, AddressingType.INDIRECT_REGISTER, Operand(RegisterType.A)),   # Прибавляем к аккумулятору значение из ячейки памяти с адресом из регистра А
        Instruction(CommandType.STA, AddressingType.REGISTER, Operand(RegisterType.C)),  # Сохраняем сумму в регистре С
        Instruction(CommandType.INC, AddressingType.REGISTER, Operand(RegisterType.A)),  # В регистре А переходим к следующему элементу массива
        Instruction(CommandType.LDA, AddressingType.REGISTER, Operand(RegisterType.A)),  # Сохраняем в аккумулятор значение регистра А
        Instruction(CommandType.CMP, AddressingType.REGISTER, Operand(RegisterType.B)),  # Сравниваем значение аккумулятора с значением последнего элемента массива
        Instruction(CommandType.LDA, AddressingType.REGISTER, Operand(RegisterType.C)),  # Загружаем в аккумудятор сумму из регистра C
        Instruction(CommandType.JNZ, AddressingType.IMMEDIATE, Operand(start_instruction_address + 5)),  # Переход к следующему элементу массива, если его конец не достигнут
        Instruction(CommandType.HLT, AddressingType.IMMEDIATE, Operand(0)),  # Завершение работы программы
    ]
    for index, instruction in enumerate(instructions):
        instruction_address = start_instruction_address + index
        memory.write(instruction_address, instruction.as_binary())
    cpu.set_start_instruction_address(start_instruction_address)
    cpu.execute_program()
    assert cpu.acc.value() == sum(arr)


