import rply

import python_dice.interface.i_pydice_lexer as i_pydice_lexer
import python_dice.interface.i_pydice_parser as i_pydice_parser
import python_dice.interface.pydice_syntax.i_dice_statement as i_dice_statement
import python_dice.src.pydice_lexer as pydice_lexer
import python_dice.src.pydice_syntax_objects as pydice_syntax_objects


class PyDiceParser(i_pydice_parser.IPyDiceParser):
    def __init__(self, lexer: i_pydice_lexer.IPyDiceLexer = None):
        if lexer is None:
            lexer = pydice_lexer.PyDiceLexer()

        self._lexer = lexer
        parser_generator = rply.ParserGenerator(
            [syntax.get_token_name() for syntax in pydice_syntax_objects.LEXER_SYNTAX],
            precedence=pydice_syntax_objects.PRECEDENCE,
        )

        for syntax in pydice_syntax_objects.LEXER_SYNTAX:
            syntax.add_production_function(parser_generator)

        self._parser = parser_generator.build()

    def parse(self, input_text: str) -> i_dice_statement.IDiceSyntax:
        return self._parser.parse(iter(self._lexer.lex(input_text)))
