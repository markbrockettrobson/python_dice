import typing

import rply  # type: ignore

from python_dice.interface.expression.i_dice_expression import IDiceExpression
from python_dice.interface.probability_distribution.i_probability_distribution import IProbabilityDistribution
from python_dice.interface.probability_distribution.i_probability_distribution_factory import (
    IProbabilityDistributionFactory,
)


class MinMaxExpression(IDiceExpression):

    TOKEN_RULE = """expression : MINMAX OPEN_PARENTHESIS expression COMMA expression CLOSE_PARENTHESIS"""
    OPERATOR_MAP = {"MAX": max, "MIN": min}

    @staticmethod
    def add_production_function(
        parser_generator: rply.ParserGenerator, probability_distribution_factory: IProbabilityDistributionFactory
    ) -> typing.Callable:
        @parser_generator.production(MinMaxExpression.TOKEN_RULE)
        def min_max(_, tokens) -> IDiceExpression:
            return MinMaxExpression(tokens[0].value, tokens[2], tokens[4])

        return min_max

    def __init__(
        self,
        min_max: str,
        expression_one: IDiceExpression,
        expression_two: IDiceExpression,
    ):
        self._min_max = min_max
        self._expression_one = expression_one
        self._expression_two = expression_two

    def roll(self) -> int:
        return self.OPERATOR_MAP[self._min_max](self._expression_one.roll(), self._expression_two.roll())

    def max(self) -> int:
        return self.OPERATOR_MAP[self._min_max](self._expression_one.max(), self._expression_two.max())

    def min(self) -> int:
        return self.OPERATOR_MAP[self._min_max](self._expression_one.min(), self._expression_two.min())

    def __str__(self) -> str:
        return f"{self._min_max}({str(self._expression_one)}, {str(self._expression_two)})"

    def estimated_cost(self) -> int:
        return self._expression_one.estimated_cost() + self._expression_two.estimated_cost()

    def get_probability_distribution(self) -> IProbabilityDistribution:
        if self._min_max == "MAX":
            return self._expression_one.get_probability_distribution().max_operator(
                self._expression_two.get_probability_distribution()
            )
        return self._expression_one.get_probability_distribution().min_operator(
            self._expression_two.get_probability_distribution()
        )

    def get_contained_variables(
        self,
    ) -> typing.Set[str]:
        return self._expression_one.get_contained_variables().union(self._expression_two.get_contained_variables())
