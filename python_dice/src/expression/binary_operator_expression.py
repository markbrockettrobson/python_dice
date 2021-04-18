import operator
import typing

import rply  # type: ignore

from python_dice.interface.expression.i_dice_expression import IDiceExpression
from python_dice.interface.probability_distribution.i_probability_distribution import IProbabilityDistribution


class BinaryOperatorExpression(IDiceExpression):
    @staticmethod
    def __equal__(this: object, other: object):
        if isinstance(this, IProbabilityDistribution) and isinstance(other, IProbabilityDistribution):
            return this.__equal__(other)
        return this == other

    @staticmethod
    def __not_equal__(this: object, other: object):
        if isinstance(this, IProbabilityDistribution) and isinstance(other, IProbabilityDistribution):
            return this.__not_equal__(other)
        return this != other

    RULE = """expression : expression BINARY_OPERATOR expression"""
    OPERATOR_MAP = {
        "==": lambda x, y: BinaryOperatorExpression.__equal__(x, y),  # pylint: disable=unnecessary-lambda
        "!=": lambda x, y: BinaryOperatorExpression.__not_equal__(x, y),  # pylint: disable=unnecessary-lambda
        "<=": operator.le,
        "<": operator.lt,
        ">=": operator.ge,
        ">": operator.gt,
        "AND": operator.and_,
        "OR": operator.or_,
    }

    @staticmethod
    def add_production_function(
        parser_generator: rply.ParserGenerator,
    ) -> typing.Callable:
        @parser_generator.production(BinaryOperatorExpression.RULE)
        def binary_operator(_, tokens) -> IDiceExpression:
            return BinaryOperatorExpression(tokens[1].value, tokens[0], tokens[2])

        return binary_operator

    def __init__(
        self,
        operator_str: str,
        expression_one: IDiceExpression,
        expression_two: IDiceExpression,
    ):
        self._operator = operator_str
        self._expression_one = expression_one
        self._expression_two = expression_two

    def roll(self) -> int:
        return 1 if self.OPERATOR_MAP[self._operator](self._expression_one.roll(), self._expression_two.roll()) else 0

    def max(self) -> int:
        return self.get_probability_distribution().max()

    def min(self) -> int:
        return self.get_probability_distribution().min()

    def __str__(self) -> str:
        return f"{str(self._expression_one)} {self._operator} {str(self._expression_two)}"

    def estimated_cost(self) -> int:
        return self._expression_one.estimated_cost() + self._expression_two.estimated_cost()

    def get_probability_distribution(self) -> IProbabilityDistribution:
        return self.OPERATOR_MAP[self._operator](
            self._expression_one.get_probability_distribution(),
            self._expression_two.get_probability_distribution(),
        )

    def get_contained_variables(
        self,
    ) -> typing.Set[str]:
        return self._expression_one.get_contained_variables().union(self._expression_two.get_contained_variables())
