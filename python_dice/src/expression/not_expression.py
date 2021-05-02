import math
import typing

import rply  # type: ignore

from python_dice.interface.expression.i_dice_expression import IDiceExpression
from python_dice.interface.probability_distribution.i_probability_distribution import IProbabilityDistribution
from python_dice.interface.probability_distribution.i_probability_distribution_factory import (
    IProbabilityDistributionFactory,
)


class NotExpression(IDiceExpression):

    TOKEN_RULE = """expression : NOT expression"""

    @staticmethod
    def add_production_function(
        parser_generator: rply.ParserGenerator, probability_distribution_factory: IProbabilityDistributionFactory
    ) -> typing.Callable:
        @parser_generator.production(NotExpression.TOKEN_RULE)
        def not_operation(_, tokens) -> IDiceExpression:
            return NotExpression(tokens[1])

        return not_operation

    def __init__(self, expression: IDiceExpression):
        self._expression = expression

    def roll(self) -> int:
        return 0 if self._expression.roll() else 1

    def max(self) -> int:
        return self.get_probability_distribution().max()

    def min(self) -> int:
        return self.get_probability_distribution().min()

    def __str__(self) -> str:
        return f"!{str(self._expression)}"

    def estimated_cost(self) -> int:
        return int(math.floor(self._expression.estimated_cost() * 1.1))

    def get_probability_distribution(self) -> IProbabilityDistribution:
        return self._expression.get_probability_distribution().not_operator()

    def get_contained_variables(
        self,
    ) -> typing.Set[str]:
        return self._expression.get_contained_variables()
