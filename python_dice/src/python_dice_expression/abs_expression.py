import typing

import rply

import python_dice.interface.python_dice_expression.i_dice_expression as i_dice_expression
import python_dice.src.probability_distribution as probability_distribution


class AbsExpression(i_dice_expression.IDiceExpression):

    TOKEN_RULE = """expression : ABS OPEN_PARENTHESIS expression CLOSE_PARENTHESIS"""

    @staticmethod
    def add_production_function(
        parser_generator: rply.ParserGenerator
    ) -> typing.Callable:
        @parser_generator.production(AbsExpression.TOKEN_RULE)
        def abs_operation(tokens) -> i_dice_expression.IDiceExpression:
            return AbsExpression(tokens[2])

        return abs_operation

    def __init__(self, expression: i_dice_expression.IDiceExpression):
        self._expression = expression

    def roll(self) -> int:
        return abs(self._expression.roll())

    def max(self) -> int:
        return self.get_probability_distribution().max()

    def min(self) -> int:
        return self.get_probability_distribution().min()

    def __str__(self) -> str:
        return f"ABS({str(self._expression)})"

    def get_probability_distribution(
        self
    ) -> probability_distribution.ProbabilityDistribution:
        return self._expression.get_probability_distribution().abs_operator()
