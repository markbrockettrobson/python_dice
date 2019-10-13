import typing

import rply

import python_dice.interface.python_dice_expression.i_dice_expression as i_dice_expression
import python_dice.src.probability_distribution as probability_distribution


class IntegerDivisionExpression(i_dice_expression.IDiceExpression):
    TOKEN_NAME = "INTEGER_DIVISION"
    TOKEN_REGEX = r"//"
    TOKEN_RULE = """expression : expression INTEGER_DIVISION expression"""

    @staticmethod
    def add_production_function(
        parser_generator: rply.ParserGenerator
    ) -> typing.Callable:
        @parser_generator.production(IntegerDivisionExpression.TOKEN_RULE)
        def integer_division(tokens) -> i_dice_expression.IDiceExpression:
            return IntegerDivisionExpression(tokens[0], tokens[2])

        return integer_division

    def __init__(
        self,
        expression_one: i_dice_expression.IDiceExpression,
        expression_two: i_dice_expression.IDiceExpression,
    ):
        self._expression_one = expression_one
        self._expression_two = expression_two

    def roll(self) -> int:
        divisor = self._expression_two.roll()
        if divisor == 0:
            raise ZeroDivisionError()
        return self._expression_one.roll() // divisor

    def max(self) -> int:
        divisor = self._expression_two.get_probability_distribution()
        if divisor.contains_zero():
            raise ZeroDivisionError(f"{str(self)}, divisor could be zero")
        return self.get_probability_distribution().max()

    def min(self) -> int:
        divisor = self._expression_two.get_probability_distribution()
        if divisor.contains_zero():
            raise ZeroDivisionError(f"{str(self)}, divisor could be zero")
        return self.get_probability_distribution().min()

    def __str__(self) -> str:
        return f"{str(self._expression_one)} // {str(self._expression_two)}"

    def get_probability_distribution(
        self
    ) -> probability_distribution.ProbabilityDistribution:
        return (
            self._expression_one.get_probability_distribution()
            // self._expression_two.get_probability_distribution()
        )
