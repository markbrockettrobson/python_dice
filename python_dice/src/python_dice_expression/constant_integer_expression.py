import typing

import rply

import python_dice.interface.python_dice_expression.i_dice_expression as i_dice_expression
import python_dice.src.probability_distribution as probability_distribution


class ConstantIntegerExpression(i_dice_expression.IDiceExpression):
    TOKEN_RULE = """expression : CONSTANT_INTEGER"""

    @staticmethod
    def add_production_function(
        parser_generator: rply.ParserGenerator
    ) -> typing.Callable:
        @parser_generator.production(ConstantIntegerExpression.TOKEN_RULE)
        def constant_integer(tokens) -> i_dice_expression.IDiceExpression:
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

    def get_probability_distribution(
        self
    ) -> probability_distribution.ProbabilityDistribution:
        return probability_distribution.ProbabilityDistribution({int(self._number): 1})