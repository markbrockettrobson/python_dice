import operator
import typing

import rply

import python_dice.interface.python_dice_expression.i_dice_expression as i_dice_expression
import python_dice.src.probability_distribution as probability_distribution


class BinaryOperatorExpression(i_dice_expression.IDiceExpression):
    RULE = """expression : expression BINARY_OPERATOR expression"""
    OPERATOR_MAP = {
        "==": operator.eq,
        "!=": operator.ne,
        "<=": operator.le,
        "<": operator.lt,
        ">=": operator.ge,
        ">": operator.gt,
        "AND": operator.and_,
        "OR": operator.or_,
    }

    @staticmethod
    def add_production_function(
        parser_generator: rply.ParserGenerator
    ) -> typing.Callable:
        @parser_generator.production(BinaryOperatorExpression.RULE)
        def binary_operator(tokens) -> i_dice_expression.IDiceExpression:
            return BinaryOperatorExpression(tokens[1].value, tokens[0], tokens[2])

        return binary_operator

    def __init__(
        self,
        operator_str: str,
        expression_one: i_dice_expression.IDiceExpression,
        expression_two: i_dice_expression.IDiceExpression,
    ):
        self._operator = operator_str
        self._expression_one = expression_one
        self._expression_two = expression_two

    def roll(self) -> int:
        return self.OPERATOR_MAP[self._operator](
            self._expression_one.roll(), self._expression_two.roll()
        )

    def max(self) -> int:
        return self.get_probability_distribution().max()

    def min(self) -> int:
        return self.get_probability_distribution().min()

    def __str__(self) -> str:
        return (
            f"{str(self._expression_one)} {self._operator} {str(self._expression_two)}"
        )

    def get_probability_distribution(
        self
    ) -> probability_distribution.ProbabilityDistribution:
        return self.OPERATOR_MAP[self._operator](
            self._expression_one.get_probability_distribution(),
            self._expression_two.get_probability_distribution(),
        )
