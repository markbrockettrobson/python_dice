import typing

import rply  # type: ignore

from python_dice.interface.expression.i_dice_expression import IDiceExpression
from python_dice.interface.probability_distribution.i_probability_distribution import IProbabilityDistribution
from python_dice.interface.probability_distribution.i_probability_distribution_factory import (
    IProbabilityDistributionFactory,
)


class ConstantBinaryExpression(IDiceExpression):
    TOKEN_RULE = """expression : CONSTANT_BINARY"""

    @staticmethod
    def add_production_function(
        parser_generator: rply.ParserGenerator, probability_distribution_factory: IProbabilityDistributionFactory
    ) -> typing.Callable:
        @parser_generator.production(ConstantBinaryExpression.TOKEN_RULE)
        def constant_binary(_, tokens) -> IDiceExpression:
            return ConstantBinaryExpression(tokens[0].value, probability_distribution_factory)

        return constant_binary

    def __init__(self, binary_string: str, probability_distribution_factory: IProbabilityDistributionFactory):
        self._binary_string = binary_string
        self._probability_distribution_factory = probability_distribution_factory

    def _get_value(self) -> int:
        return 1 if self._binary_string == "True" else 0

    def roll(self) -> int:
        return self._get_value()

    def max(self) -> int:
        return self._get_value()

    def min(self) -> int:
        return self._get_value()

    def __str__(self) -> str:
        return self._binary_string

    def estimated_cost(self) -> int:
        return 2

    def get_probability_distribution(self) -> IProbabilityDistribution:
        return self._probability_distribution_factory.create({self._get_value(): 1})

    def get_contained_variables(
        self,
    ) -> typing.Set[str]:
        return set()
