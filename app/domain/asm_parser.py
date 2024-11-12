from typing import Dict, List

from domain.memory import Memory
from schemas.instruction import Instruction


class ASMParser:

    def __init__(self, ):
        self.code_line_by_label: Dict[str, int] = {}
        self.code_line_counter = 0

    def load_program_to_memory(self, text: str, memory: Memory):
        data_section = text[:text.find('.code')].strip()
        code_section = text[text.find('.code\n') + 6:].strip()
        data = self.parse_data_section(data_section, )
        code = self.parse_code_section(code_section, len(data))
        for index, value in enumerate(*data, *code):
            memory.write(index, value)

    def parse_data_section(self, data_section: str, ) -> List[int]:
        numbers = data_section.strip().replace('\n', '').split('num')
        if '' in numbers:
            numbers.remove('')
        return list(map(lambda n: int(n), numbers))

    def parse_code_section(self, code_section: str, instruction_offset: int) -> List[int]:
        code_lines = code_section.split('\n')
        if '' in code_lines:
            code_lines.remove('')
        instructions = []
        for index, code_line in enumerate(code_lines):
            if ':' in code_line and ' ' not in code_line:  # Получена метка
                label = code_line.strip().replace(':', '')
                self.code_line_by_label[label] = instruction_offset + index - len(self.code_line_by_label)
                continue
            try:
                instruction = Instruction.from_text(code_line)
            except ValueError:
                instruction = None
                for label, code_line_index in self.code_line_by_label.items():
                    if label in code_line:
                        instruction = Instruction.from_text(code_line.replace(label, str(code_line_index)))
                if not instruction:
                    raise ValueError(f"Неизвестная команда: {code_line}")
            instructions.append(instruction)
        return [instruction.as_binary() for instruction in instructions]