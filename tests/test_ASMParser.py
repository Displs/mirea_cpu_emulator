import pprint

from domain.asm_parser import ASMParser


def test_parse_data_section():
    asm_parser = ASMParser()
    data_section = asm_parser.parse_data_section("num 1\nnum 2\n num 3")
    pprint.pprint(data_section)
    for index, number in enumerate([1, 2, 3]):
        assert number == data_section[index]


def test_parse_code_section():
    asm_parser = ASMParser()
    code_section = asm_parser.parse_code_section("LDA ?1\nSTA /A\nADD ?0")
    pprint.pprint(code_section)

