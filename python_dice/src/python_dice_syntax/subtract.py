import typing

import rply

import python_dice.interface.python_dice_syntax.i_dice_statement as i_dice_statement
import python_dice.src.probability_distribution as probability_distribution


class Subtract(i_dice_statement.IDiceSyntax):
    TOKEN_NAME = "SUBTRACT"
    TOKEN_REGEX = r"\-"
    TOKEN_RULE = """expression : expression SUBTRACT expression"""

    @staticmethod
    def add_production_function(
        parser_generator: rply.ParserGenerator
    ) -> typing.Callable:
        @parser_generator.production(Subtract.TOKEN_RULE)
        def subtract(tokens) -> i_dice_statement.IDiceSyntax:
            return Subtract(tokens[0], tokens[2])

        return subtract

    @staticmethod
    def get_token_name() -> str:
        return Subtract.TOKEN_NAME

    @staticmethod
    def get_token_regex() -> str:
        return Subtract.TOKEN_REGEX

    def __init__(
        self,
        expression_one: i_dice_statement.IDiceSyntax,
        expression_two: i_dice_statement.IDiceSyntax,
    ):
        self._expression_one = expression_one
        self._expression_two = expression_two

    def roll(self) -> int:
        return self._expression_one.roll() - self._expression_two.roll()

    def max(self) -> int:
        return self.get_probability_distribution().max()

    def min(self) -> int:
        return self.get_probability_distribution().min()

    def __str__(self) -> str:
        return f"{str(self._expression_one)} - {str(self._expression_two)}"

    def get_probability_distribution(
        self
    ) -> probability_distribution.ProbabilityDistribution:
        return (
            self._expression_one.get_probability_distribution()
            - self._expression_two.get_probability_distribution()
        )
