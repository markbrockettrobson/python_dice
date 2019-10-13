import typing

import rply

import python_dice.interface.python_dice_expression.i_dice_expression as i_dice_expression
import python_dice.src.probability_distribution as probability_distribution


class NotExpression(i_dice_expression.IDiceExpression):

    TOKEN_RULE = """expression : NOT expression"""

    @staticmethod
    def add_production_function(
        parser_generator: rply.ParserGenerator
    ) -> typing.Callable:
        @parser_generator.production(NotExpression.TOKEN_RULE)
        def not_operation(tokens) -> i_dice_expression.IDiceExpression:
            return NotExpression(tokens[1])

        return not_operation

    def __init__(self, expression: i_dice_expression.IDiceExpression):
        self._expression = expression

    def roll(self) -> int:
        return 0 if self._expression.roll() else 1

    def max(self) -> int:
        return self.get_probability_distribution().max()

    def min(self) -> int:
        return self.get_probability_distribution().min()

    def __str__(self) -> str:
        return f"!{str(self._expression)}"

    def get_probability_distribution(
        self
    ) -> probability_distribution.ProbabilityDistribution:
        return self._expression.get_probability_distribution().not_operator()
