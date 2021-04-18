import typing

import rply  # type: ignore

from python_dice.interface.expression.i_dice_expression import IDiceExpression
from python_dice.interface.probability_distribution.i_probability_distribution import IProbabilityDistribution


class AddExpression(IDiceExpression):
    RULE = """expression : expression ADD expression"""

    @staticmethod
    def add_production_function(
        parser_generator: rply.ParserGenerator,
    ) -> typing.Callable:
        @parser_generator.production(AddExpression.RULE)
        def add(_, tokens) -> IDiceExpression:
            return AddExpression(tokens[0], tokens[2])

        return add

    def __init__(
        self,
        expression_one: IDiceExpression,
        expression_two: IDiceExpression,
    ):
        self._expression_one = expression_one
        self._expression_two = expression_two

    def roll(self) -> int:
        return self._expression_one.roll() + self._expression_two.roll()

    def max(self) -> int:
        return self.get_probability_distribution().max()

    def min(self) -> int:
        return self.get_probability_distribution().min()

    def __str__(self) -> str:
        return f"{str(self._expression_one)} + {str(self._expression_two)}"

    def estimated_cost(self) -> int:
        return self._expression_one.estimated_cost() + self._expression_two.estimated_cost()

    def get_probability_distribution(self) -> IProbabilityDistribution:
        return self._expression_one.get_probability_distribution() + self._expression_two.get_probability_distribution()

    def get_contained_variables(
        self,
    ) -> typing.Set[str]:
        return self._expression_one.get_contained_variables().union(self._expression_two.get_contained_variables())
