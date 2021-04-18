import typing

import rply  # type: ignore

from python_dice.interface.expression.i_dice_expression import IDiceExpression
from python_dice.interface.probability_distribution.i_probability_distribution import IProbabilityDistribution
from python_dice.src.probability_distribution.probability_distribution import ProbabilityDistribution


class ConstantIntegerExpression(IDiceExpression):
    TOKEN_RULE = """expression : CONSTANT_INTEGER"""

    @staticmethod
    def add_production_function(
        parser_generator: rply.ParserGenerator,
    ) -> typing.Callable:
        @parser_generator.production(ConstantIntegerExpression.TOKEN_RULE)
        def constant_integer(_, tokens) -> IDiceExpression:
            return ConstantIntegerExpression(tokens[0].value)

        return constant_integer

    def __init__(self, number: str):
        self._number = number

    def roll(self) -> int:
        return int(self._number)

    def max(self) -> int:
        return int(self._number)

    def min(self) -> int:
        return int(self._number)

    def __str__(self) -> str:
        return self._number

    def estimated_cost(self) -> int:
        return 2

    def get_probability_distribution(self) -> IProbabilityDistribution:
        return ProbabilityDistribution({int(self._number): 1})

    def get_contained_variables(
        self,
    ) -> typing.Set[str]:
        return set()
