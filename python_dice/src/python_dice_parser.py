from typing import Optional, Tuple

import rply  # type: ignore

from python_dice.interface.expression.i_dice_expression import IDiceExpression
from python_dice.interface.i_python_dice_lexer import IPythonDiceLexer
from python_dice.interface.i_python_dice_parser import IPythonDiceParser
from python_dice.interface.probability_distribution.i_probability_distribution_factory import (
    IProbabilityDistributionFactory,
)
from python_dice.interface.probability_distribution.i_probability_distribution_state import (
    IProbabilityDistributionState,
)
from python_dice.interface.probability_distribution.i_probability_distribution_state_factory import (
    IProbabilityDistributionStateFactory,
)
from python_dice.src.probability_distribution.probability_distribution_factory import ProbabilityDistributionFactory
from python_dice.src.probability_distribution.probability_distribution_state import ProbabilityDistributionState
from python_dice.src.probability_distribution.probability_distribution_state_factory import (
    ProbabilityDistributionStateFactory,
)
from python_dice.src.python_dice_lexer import PythonDiceLexer
from python_dice.src.python_dice_syntax_objects import LEXER_SYNTAX, PARSER_EXPRESSIONS, PRECEDENCE


class PythonDiceParser(IPythonDiceParser):
    def __init__(
        self,
        lexer: Optional[IPythonDiceLexer] = None,
        probability_distribution_factory: Optional[IProbabilityDistributionFactory] = None,
        probability_distribution_state_factory: Optional[IProbabilityDistributionStateFactory] = None,
    ):
        if lexer is None:
            lexer = PythonDiceLexer()
        if probability_distribution_factory is None:
            probability_distribution_factory = ProbabilityDistributionFactory()
        if probability_distribution_state_factory is None:
            probability_distribution_state_factory = ProbabilityDistributionStateFactory()
        self._lexer = lexer
        parser_generator = rply.ParserGenerator(
            [syntax.get_token_name() for syntax in LEXER_SYNTAX],
            precedence=PRECEDENCE,
        )

        for syntax in PARSER_EXPRESSIONS:
            syntax.add_production_function(parser_generator, probability_distribution_factory)

        #  pylint: disable=unused-variable
        @parser_generator.error
        def error_handler(_: ProbabilityDistributionState, token: rply.token.Token):
            raise ValueError(
                "Ran into a %s (%s) where it wasn't expected, at position %s."
                % (token.gettokentype(), token.getstr(), token.getsourcepos())
            )

        self._parser = parser_generator.build()
        self._probability_distribution_state_factory = probability_distribution_state_factory

    def parse(
        self,
        input_text: str,
        state: IProbabilityDistributionState = None,
    ) -> Tuple[IDiceExpression, IProbabilityDistributionState,]:
        if state is None:
            state = self._probability_distribution_state_factory.create_new_empty_set()
        return self._parser.parse(iter(self._lexer.lex(input_text)), state=state), state
