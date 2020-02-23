import random
import re
import typing

import rply

import python_dice.interface.i_probability_distribution as i_probability_distribution
import python_dice.interface.python_dice_expression.i_dice_expression as i_dice_expression
import python_dice.src.probability_distribution as probability_distribution


class DiceExpression(i_dice_expression.IDiceExpression):
    TOKEN_RULE = """expression : DICE"""

    @staticmethod
    def add_production_function(
        parser_generator: rply.ParserGenerator
    ) -> typing.Callable:
        @parser_generator.production(DiceExpression.TOKEN_RULE)
        def dice(_, tokens) -> i_dice_expression.IDiceExpression:
            return DiceExpression(tokens[0].value)

        return dice

    def __init__(self, string_form: str):
        self._string_form = string_form
        self._single_dice_outcome_map = self._get_single_dice_outcome_map()
        self._number_of_dice = self._get_number_of_dice()

    def _get_number_of_dice(self) -> int:
        string_num = self._string_form.split("d")[0]
        return 1 if string_num == "" else int(string_num)

    def _get_single_dice_outcome_map(self) -> typing.Dict[int, int]:
        def save_add(dictionary, value):
            if value not in dictionary:
                dictionary[value] = 0
            dictionary[value] += 1

        string_num = self._string_form.split("d")[1]
        if re.match(r"\d+", string_num) is not None:
            value_dictionary = {value: 1 for value in range(1, int(string_num) + 1)}
        elif string_num == "%":
            value_dictionary = {value: 1 for value in range(1, 100 + 1)}
        elif string_num == "F":
            value_dictionary = {-1: 1, 0: 1, 1: 1}
        else:
            number_list = [
                int(value)
                for value in re.split(r",", re.sub(r"(\[|\]|\s+)", "", string_num))
            ]
            value_dictionary = {}
            for number in number_list:
                save_add(value_dictionary, number)
        return value_dictionary

    def roll(self) -> int:
        return sum(
            random.choices(
                list(self._single_dice_outcome_map.keys()),
                weights=list(self._single_dice_outcome_map.values()),
                k=self._number_of_dice,
            )
        )

    def max(self) -> int:
        return (max(self._single_dice_outcome_map.keys())) * self._number_of_dice

    def min(self) -> int:
        return (min(self._single_dice_outcome_map.keys())) * self._number_of_dice

    def __str__(self) -> str:
        return f"{self._string_form}"

    def get_probability_distribution(
        self
    ) -> i_probability_distribution.IProbabilityDistribution:
        single_dice_distribution = probability_distribution.ProbabilityDistribution(
            self._get_single_dice_outcome_map()
        )
        distribution = probability_distribution.ProbabilityDistribution(
            single_dice_distribution.get_result_map()
        )
        for _ in range(0, self._number_of_dice - 1):
            distribution = distribution + single_dice_distribution
        return distribution
