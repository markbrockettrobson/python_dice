import typing

import rply

import python_dice.interface.python_dice_syntax.i_dice_statement as i_dice_statement
import python_dice.src.probability_distribution as probability_distribution


class Add(i_dice_statement.IDiceSyntax):
    TOKEN_NAME = "ADD"
    TOKEN_REGEX = r"\+"
    TOKEN_RULE = """expression : expression ADD expression"""

    @staticmethod
    def add_production_function(
        parser_generator: rply.ParserGenerator
    ) -> typing.Callable:
        @parser_generator.production(Add.TOKEN_RULE)
        def add(tokens) -> i_dice_statement.IDiceSyntax:
            return Add(tokens[0], tokens[2])

        return add

    @staticmethod
    def get_token_name() -> str:
        return Add.TOKEN_NAME

    @staticmethod
    def get_token_regex() -> str:
        return Add.TOKEN_REGEX

    def __init__(
        self,
        expression_one: i_dice_statement.IDiceSyntax,
        expression_two: i_dice_statement.IDiceSyntax,
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

    def get_probability_distribution(
        self
    ) -> probability_distribution.ProbabilityDistribution:
        return (
            self._expression_one.get_probability_distribution()
            + self._expression_two.get_probability_distribution()
        )
