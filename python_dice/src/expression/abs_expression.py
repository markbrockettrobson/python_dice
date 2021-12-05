from typing import Callable, Set

import rply  # type: ignore

from python_dice.interface.expression.i_dice_expression import IDiceExpression
from python_dice.interface.probability_distribution.i_probability_distribution import IProbabilityDistribution
from python_dice.interface.probability_distribution.i_probability_distribution_factory import (
    IProbabilityDistributionFactory,
)


class AbsExpression(IDiceExpression):
    TOKEN_RULE = """expression : ABS OPEN_PARENTHESIS expression CLOSE_PARENTHESIS"""

    @staticmethod
    def add_production_function(
        parser_generator: rply.ParserGenerator, probability_distribution_factory: IProbabilityDistributionFactory
    ) -> Callable:
        @parser_generator.production(AbsExpression.TOKEN_RULE)
        def abs_operation(_, tokens) -> IDiceExpression:
            return AbsExpression(tokens[2])

        return abs_operation

    def __init__(self, expression: IDiceExpression):
        self._expression = expression

    def roll(self) -> int:
        return abs(self._expression.roll())

    def max(self) -> int:
        return self.get_probability_distribution().max()

    def min(self) -> int:
        return self.get_probability_distribution().min()

    def __str__(self) -> str:
        return f"ABS({str(self._expression)})"

    def estimated_cost(self) -> int:
        return self._expression.estimated_cost()

    def get_probability_distribution(self) -> IProbabilityDistribution:
        return abs(self._expression.get_probability_distribution())

    def get_contained_variables(
        self,
    ) -> Set[str]:
        return self._expression.get_contained_variables()
