import typing

import rply

import python_dice.interface.python_dice_syntax.i_dice_statement as i_dice_statement


class Multiply(i_dice_statement.IDiceSyntax):
    TOKEN_NAME = "MULTIPLY"
    TOKEN_REGEX = r"\*"
    TOKEN_RULE = """expression : expression MULTIPLY expression"""

    @staticmethod
    def add_production_function(
        parser_generator: rply.ParserGenerator
    ) -> typing.Callable:
        @parser_generator.production(Multiply.TOKEN_RULE)
        def multiply(tokens) -> i_dice_statement.IDiceSyntax:
            return Multiply(tokens[0], tokens[2])

        return multiply

    @staticmethod
    def get_token_name() -> str:
        return Multiply.TOKEN_NAME

    @staticmethod
    def get_token_regex() -> str:
        return Multiply.TOKEN_REGEX

    def __init__(
        self,
        expression_one: i_dice_statement.IDiceSyntax,
        expression_two: i_dice_statement.IDiceSyntax,
    ):
        self._expression_one = expression_one
        self._expression_two = expression_two

    def roll(self) -> int:
        return self._expression_one.roll() * self._expression_two.roll()

    def max(self) -> int:
        return self._expression_one.max() * self._expression_two.max()

    def min(self) -> int:
        return self._expression_one.min() * self._expression_two.min()

    def __str__(self) -> str:
        return f"{str(self._expression_one)} * {str(self._expression_two)}"
