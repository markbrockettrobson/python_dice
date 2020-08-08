import typing

import rply

import python_dice.interface.i_python_dice_lexer as i_pydice_lexer
import python_dice.src.python_dice_syntax_objects as pydice_syntax_objects


class PythonDiceLexer(i_pydice_lexer.IPythonDiceLexer):
    def __init__(self):
        partial_lexer = rply.LexerGenerator()
        for syntax in pydice_syntax_objects.LEXER_SYNTAX:
            partial_lexer.add(syntax.get_token_name(), syntax.get_token_regex())
        # Ignore spaces
        partial_lexer.ignore(r"\s+")
        self._lexer = partial_lexer.build()

    def lex(self, input_text: str) -> typing.List[rply.Token]:
        return list(self._lexer.lex(input_text))
