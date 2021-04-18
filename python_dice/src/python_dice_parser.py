import typing

import rply  # type: ignore

import python_dice.interface.expression.i_dice_expression as i_dice_expression
import python_dice.interface.i_python_dice_lexer as i_pydice_lexer
import python_dice.interface.i_python_dice_parser as i_pydice_parser
import python_dice.interface.probability_distribution.i_probability_distribution_state as i_probability_state
import python_dice.src.probability_distribution.probability_state as probability_state
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

        for syntax in pydice_syntax_objects.PARSER_EXPRESSIONS:
            syntax.add_production_function(parser_generator)

        #  pylint: disable=unused-variable
        @parser_generator.error
        def error_handler(_: probability_state.ProbabilityState, token: rply.token.Token):
            raise ValueError(
                "Ran into a %s (%s) where it wasn't expected, at position %s."
                % (token.gettokentype(), token.getstr(), token.getsourcepos())
            )

        self._parser = parser_generator.build()

    def parse(
        self,
        input_text: str,
        state: i_probability_state.IProbabilityDistributionState = None,
    ) -> typing.Tuple[i_dice_expression.IDiceExpression, i_probability_state.IProbabilityDistributionState,]:
        if state is None:
            state = probability_state.ProbabilityState()
        return self._parser.parse(iter(self._lexer.lex(input_text)), state=state), state
