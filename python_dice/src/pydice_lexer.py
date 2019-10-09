import typing

import rply

import python_dice.interface.i_pydice_lexer as i_pydice_lexer
import python_dice.src.dice_statement.constant_integer as constant_integer


class PyDiceLexer(i_pydice_lexer.IPyDiceLexer):

    LEXER_SYNTAX = [constant_integer.ConstantInteger]

    def __init__(self):
        partial_lexer = rply.LexerGenerator()
        for syntax in PyDiceLexer.LEXER_SYNTAX:
            partial_lexer.add(syntax.get_token_name(), syntax.get_token_regex())
        # Ignore spaces
        partial_lexer.ignore(r"\s+")
        self._lexer = partial_lexer.build()

    def lex(self, input_text: str) -> typing.List[rply.Token]:
        return [token for token in self._lexer.lex(" " + input_text + " ")]
