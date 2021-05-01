import typing

import rply  # type: ignore

from python_dice.interface.expression.i_dice_expression import IDiceExpression
from python_dice.interface.probability_distribution.i_probability_distribution import IProbabilityDistribution
from python_dice.interface.probability_distribution.i_probability_distribution_factory import (
    IProbabilityDistributionFactory,
)


class ParenthesisEnclosedExpression(IDiceExpression):
    RULE = """expression : OPEN_PARENTHESIS expression CLOSE_PARENTHESIS"""

    @staticmethod
    def add_production_function(
        parser_generator: rply.ParserGenerator, probability_distribution_factory: IProbabilityDistributionFactory
    ) -> typing.Callable:
        @parser_generator.production(ParenthesisEnclosedExpression.RULE)
        def parenthesis_enclosed(_, tokens) -> IDiceExpression:
            return ParenthesisEnclosedExpression(tokens[1])

        return parenthesis_enclosed

    def __init__(self, expression: IDiceExpression):
        self._expression = expression

    def roll(self) -> int:
        return self._expression.roll()

    def max(self) -> int:
        return self._expression.max()

    def min(self) -> int:
        return self._expression.min()

    def __str__(self) -> str:
        return f"({str(self._expression)})"

    def estimated_cost(self) -> int:
        return self._expression.estimated_cost()

    def get_probability_distribution(self) -> IProbabilityDistribution:
        return self._expression.get_probability_distribution()

    def get_contained_variables(
        self,
    ) -> typing.Set[str]:
        return self._expression.get_contained_variables()
