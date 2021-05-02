import typing

import rply  # type: ignore

from python_dice.interface.i_python_dice_lexer import IPythonDiceLexer
from python_dice.src.python_dice_syntax_objects import LEXER_SYNTAX


class PythonDiceLexer(IPythonDiceLexer):
    def __init__(self):
        partial_lexer = rply.LexerGenerator()
        for syntax in LEXER_SYNTAX:
            partial_lexer.add(syntax.get_token_name(), syntax.get_token_regex())
        # Ignore spaces
        partial_lexer.ignore(r"\s+")
        self._lexer = partial_lexer.build()

    def lex(self, input_text: str) -> typing.List[rply.Token]:
        try:
            return list(self._lexer.lex(input_text))
        except rply.errors.LexingError as exception:
            input_lines = input_text.split("\n")
            source_column_number = exception.getsourcepos().idx

            current_line_index = 0
            while len(input_lines[current_line_index]) < source_column_number:
                source_column_number -= len(input_lines[current_line_index]) + 1
                current_line_index += 1

            sub_string_start = max(0, source_column_number - 50)
            sub_string_end = min(len(input_text), source_column_number + 50)

            sub_string = input_lines[current_line_index][sub_string_start:sub_string_end]
            arrow_line = "-" * (source_column_number - sub_string_start) + "^"
            message = f"{sub_string}\n{arrow_line}"

            new_exception = ValueError(message)
        raise new_exception
