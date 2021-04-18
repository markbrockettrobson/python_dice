import random
import typing

import rply  # type: ignore

from python_dice.interface.expression.i_dice_expression import IDiceExpression
from python_dice.interface.probability_distribution.i_probability_distribution import IProbabilityDistribution
from python_dice.src.expression.dice_expression_helper import get_single_dice_outcome_map
from python_dice.src.probability_distribution.probability_distribution import ProbabilityDistribution


class DiceExpression(IDiceExpression):
    TOKEN_RULE = """expression : DICE"""

    @staticmethod
    def add_production_function(
        parser_generator: rply.ParserGenerator,
    ) -> typing.Callable:
        @parser_generator.production(DiceExpression.TOKEN_RULE)
        def dice(_, tokens) -> IDiceExpression:
            return DiceExpression(tokens[0].value)

        return dice

    def __init__(self, string_form: str):
        self._string_form = string_form
        self._single_dice_outcome_map = get_single_dice_outcome_map(self._string_form.split("d")[1])
        self._number_of_dice = self._get_number_of_dice()

    def _get_number_of_dice(self) -> int:
        string_num = self._string_form.split("d")[0]
        return 1 if string_num == "" else int(string_num)

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

    def estimated_cost(self) -> int:
        return self._number_of_dice * len(self._single_dice_outcome_map.values())

    def __str__(self) -> str:
        return f"{self._string_form}"

    def get_probability_distribution(self) -> IProbabilityDistribution:
        single_dice_distribution: IProbabilityDistribution = ProbabilityDistribution(self._single_dice_outcome_map)
        distribution: IProbabilityDistribution = ProbabilityDistribution(single_dice_distribution.get_result_map())
        for _ in range(0, self._number_of_dice - 1):
            distribution = distribution + single_dice_distribution
        return distribution

    def get_contained_variables(
        self,
    ) -> typing.Set[str]:
        return set()
