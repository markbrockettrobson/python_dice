import typing

import numpy
import rply

import python_dice.interface.python_dice_syntax.i_dice_statement as i_dice_statement
import python_dice.src.probability_distribution as probability_distribution


class Dice(i_dice_statement.IDiceSyntax):
    TOKEN_NAME = "DICE"
    TOKEN_REGEX = r"\d+d\d+"
    TOKEN_RULE = """expression : DICE"""

    @staticmethod
    def add_production_function(
        parser_generator: rply.ParserGenerator
    ) -> typing.Callable:
        @parser_generator.production(Dice.TOKEN_RULE)
        def dice(tokens) -> i_dice_statement.IDiceSyntax:
            return Dice(tokens[0].value)

        return dice

    @staticmethod
    def get_token_name() -> str:
        return Dice.TOKEN_NAME

    @staticmethod
    def get_token_regex() -> str:
        return Dice.TOKEN_REGEX

    def __init__(self, string_form: str):
        self._string_form = string_form

    def _get_number_of_dice(self) -> int:
        return int(self._string_form.split("d")[0])

    def _get_number_of_sides(self) -> int:
        return int(self._string_form.split("d")[1])

    def roll(self) -> int:
        return sum(
            numpy.random.randint(
                1, self._get_number_of_sides() + 1, self._get_number_of_dice()
            )
        )

    def max(self) -> int:
        return (self._get_number_of_sides()) * self._get_number_of_dice()

    def min(self) -> int:
        return self._get_number_of_dice()

    def __str__(self) -> str:
        return f"{self._string_form}"

    def get_probability_distribution(
        self
    ) -> probability_distribution.ProbabilityDistribution:
        single_dice_distribution = probability_distribution.ProbabilityDistribution(
            {value: 1 for value in range(1, self._get_number_of_sides() + 1)}
        )
        distribution = probability_distribution.ProbabilityDistribution(
            single_dice_distribution.get_result_map()
        )
        for _ in range(0, self._get_number_of_dice() - 1):
            distribution = distribution + single_dice_distribution
        return distribution
