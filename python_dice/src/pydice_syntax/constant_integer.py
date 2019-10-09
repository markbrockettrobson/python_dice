import typing

import rply

import python_dice.interface.pydice_syntax.i_dice_statement as i_dice_statement


class ConstantInteger(i_dice_statement.IDiceSyntax):
    TOKEN_NAME = "CONSTANT_INTEGER"
    TOKEN_REGEX = r"-?\d+"
    TOKEN_RULE = """expression : CONSTANT_INTEGER"""

    @staticmethod
    def add_production_function(
        parser_generator: rply.ParserGenerator
    ) -> typing.Callable:
        @parser_generator.production(ConstantInteger.TOKEN_RULE)
        def constant_integer(tokens) -> i_dice_statement.IDiceSyntax:
            return ConstantInteger(tokens[0].value)

        return constant_integer

    @staticmethod
    def get_token_name() -> str:
        return ConstantInteger.TOKEN_NAME

    @staticmethod
    def get_token_regex() -> str:
        return ConstantInteger.TOKEN_REGEX

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
