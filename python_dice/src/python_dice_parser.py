import rply

import python_dice.interface.i_python_dice_lexer as i_pydice_lexer
import python_dice.interface.i_python_dice_parser as i_pydice_parser
import python_dice.interface.python_dice_expression.i_dice_expression as i_dice_expression
import python_dice.src.python_dice_lexer as pydice_lexer
import python_dice.src.python_dice_syntax_objects as pydice_syntax_objects


class PythonDiceParser(i_pydice_parser.IPythonDiceParser):
    def __init__(self, lexer: i_pydice_lexer.IPythonDiceLexer = None):
        if lexer is None:
            lexer = pydice_lexer.PythonDiceLexer()

        self._lexer = lexer
        parser_generator = rply.ParserGenerator(
            [syntax.get_token_name() for syntax in pydice_syntax_objects.LEXER_SYNTAX],
            precedence=pydice_syntax_objects.PRECEDENCE,
        )

        for syntax in pydice_syntax_objects.LEXER_Expression:
            syntax.add_production_function(parser_generator)

        self._parser = parser_generator.build()

    def parse(self, input_text: str) -> i_dice_expression.IDiceExpression:
        return self._parser.parse(iter(self._lexer.lex(input_text)))
