import random
import re
from typing import Callable, Dict, List, Set

import rply  # type: ignore

from python_dice.interface.expression.i_dice_expression import IDiceExpression
from python_dice.interface.probability_distribution.i_probability_distribution import IProbabilityDistribution
from python_dice.interface.probability_distribution.i_probability_distribution_factory import (
    IProbabilityDistributionFactory,
)
from python_dice.src.expression.constant_integer_expression import ConstantIntegerExpression
from python_dice.src.expression.dice_expression import DiceExpression
from python_dice.src.expression.dice_expression_helper import get_single_dice_outcome_map


class DropKeepExpression(IDiceExpression):
    TOKEN_RULE = """expression : DROP_KEEP_DICE"""

    @staticmethod
    def add_production_function(
        parser_generator: rply.ParserGenerator, probability_distribution_factory: IProbabilityDistributionFactory
    ) -> Callable:
        @parser_generator.production(DropKeepExpression.TOKEN_RULE)
        def drop_keep(_, tokens) -> IDiceExpression:
            return DropKeepExpression(tokens[0].value, probability_distribution_factory)

        return drop_keep

    def __init__(self, string_form: str, probability_distribution_factory: IProbabilityDistributionFactory):
        self._string_form = string_form
        self._number_of_dice = self._get_number_of_dice()
        self._single_dice_outcome_map = get_single_dice_outcome_map(re.split(r"[dk]", self._string_form)[1])
        self._number_to_keep_or_drop = self._get_number_to_keep_or_drop()
        self._simplified_form = None
        self._probability_distribution_factory = probability_distribution_factory

        if self._is_keep():
            if self._number_of_dice <= self._number_to_keep_or_drop:
                self._simplified_form = DiceExpression(
                    f"{self._number_of_dice}d{self._get_number_of_sides_string()}",
                    self._probability_distribution_factory,
                )
            elif self._number_to_keep_or_drop == 0:
                self._simplified_form = ConstantIntegerExpression("0", self._probability_distribution_factory)
        else:
            if self._number_of_dice <= self._number_to_keep_or_drop:
                self._simplified_form = ConstantIntegerExpression("0", self._probability_distribution_factory)
            elif self._number_to_keep_or_drop == 0:
                self._simplified_form = DiceExpression(
                    f"{self._number_of_dice}d{self._get_number_of_sides_string()}",
                    self._probability_distribution_factory,
                )

    def _get_number_of_dice(self) -> int:
        string_num = re.split(r"[dk]", self._string_form)[0]
        return 1 if string_num == "" else int(string_num)

    def _get_number_to_keep_or_drop(self) -> int:
        return int(re.split(r"[dk]", self._string_form)[2])

    def _get_number_of_sides_string(self) -> str:
        return re.split(r"[dk]", self._string_form)[1]

    def _is_keep(self) -> bool:
        return "k" in self._string_form

    def roll(self) -> int:
        if self._simplified_form is not None:
            return self._simplified_form.roll()

        dice_rolls = random.choices(
            list(self._single_dice_outcome_map.keys()),
            weights=list(self._single_dice_outcome_map.values()),
            k=self._number_of_dice,
        )
        dice_rolls.sort()
        if self._is_keep():
            return sum(dice_rolls[-self._number_to_keep_or_drop :])
        return sum(dice_rolls[: self._number_of_dice - self._number_to_keep_or_drop])

    def max(self) -> int:
        if self._simplified_form is not None:
            return self._simplified_form.max()

        if self._is_keep():
            return self._number_to_keep_or_drop * max(self._single_dice_outcome_map.keys())
        return (self._number_of_dice - self._number_to_keep_or_drop) * max(self._single_dice_outcome_map.keys())

    def min(self) -> int:
        if self._simplified_form is not None:
            return self._simplified_form.min()

        if self._is_keep():
            return self._number_to_keep_or_drop * min(self._single_dice_outcome_map.keys())
        return (self._number_of_dice - self._number_to_keep_or_drop) * min(self._single_dice_outcome_map.keys())

    def __str__(self) -> str:
        return f"{self._string_form}"

    def estimated_cost(self) -> int:
        if self._simplified_form is not None:
            return self._simplified_form.estimated_cost()

        if self._is_keep():
            return (self._number_of_dice * self._number_to_keep_or_drop) * len(self._single_dice_outcome_map.values())
        return (self._number_of_dice * (self._number_of_dice - self._number_to_keep_or_drop)) * len(
            self._single_dice_outcome_map.values()
        )

    def get_probability_distribution(self) -> IProbabilityDistribution:
        if self._simplified_form is not None:
            return self._simplified_form.get_probability_distribution()

        is_keep = self._is_keep()
        number_of_dice_to_select = self._number_of_dice - self._number_to_keep_or_drop
        number_of_dice_remaining = self._number_to_keep_or_drop
        if is_keep:
            number_of_dice_to_select = self._number_to_keep_or_drop
            number_of_dice_remaining = self._number_of_dice - self._number_to_keep_or_drop

        current = DropKeepExpression._build_dice_dict(number_of_dice_to_select, self._single_dice_outcome_map)
        current = DropKeepExpression._compute_iterations(
            current, number_of_dice_remaining, self._single_dice_outcome_map, is_keep
        )

        out_come_map = DropKeepExpression._collapse_outcomes(current)
        return self._probability_distribution_factory.create(out_come_map)

    @staticmethod
    def _build_dice_dict(number_of_dice: int, dice_outcome_map: Dict[int, int]) -> Dict[str, int]:
        def safe_add_to_dict(dictionary: Dict[str, int], key: str, value: int) -> None:
            if key not in dictionary:
                dictionary[key] = 0
            dictionary[key] += value

        current_dict = {"": 1}
        for _ in range(number_of_dice):
            new_dict: Dict[str, int] = {}
            for dice_outcome, count in dice_outcome_map.items():
                for old_key, old_value in current_dict.items():
                    new_key = DropKeepExpression._string_key_to_list(old_key)
                    new_key.append(dice_outcome)
                    new_key.sort()
                    safe_add_to_dict(
                        new_dict,
                        DropKeepExpression._int_list_to_string(new_key),
                        old_value * count,
                    )
            current_dict = new_dict
        return current_dict

    @staticmethod
    def _string_key_to_list(string: str) -> List[int]:
        if string == "":
            return []
        return [int(n) for n in string.split("|")]

    @staticmethod
    def _int_list_to_string(values: List[int]) -> str:
        values.sort()
        return "|".join([str(n) for n in values])

    @staticmethod
    def _update_key_list(old_key_string: str, new_value: int, is_keep: bool) -> str:
        old_value = DropKeepExpression._string_key_to_list(old_key_string)
        old_value.append(new_value)
        old_value.sort()
        if is_keep:
            old_value = old_value[1:]
        else:
            old_value = old_value[:-1]
        return DropKeepExpression._int_list_to_string(old_value)

    @staticmethod
    def _compute_iterations(
        current: Dict[str, int],
        number_of_dice: int,
        dice_outcome_map: Dict[int, int],
        is_keep: bool,
    ) -> Dict[str, int]:
        def safe_add_to_dict(dictionary: Dict[str, int], key: str, value: int) -> None:
            if key not in dictionary:
                dictionary[key] = 0
            dictionary[key] += value

        current_dict = current
        for _ in range(number_of_dice):
            new_dict: Dict[str, int] = {}
            for dice_outcome, count in dice_outcome_map.items():
                for old_key, old_value in current_dict.items():
                    new_key = DropKeepExpression._update_key_list(old_key, dice_outcome, is_keep)
                    safe_add_to_dict(new_dict, new_key, old_value * count)
            current_dict = new_dict
        return current_dict

    @staticmethod
    def _collapse_outcomes(outcomes: Dict[str, int]) -> Dict[int, int]:
        def safe_add_to_dict(dictionary: Dict[int, int], key: int, value: int) -> None:
            if key not in dictionary:
                dictionary[key] = 0
            dictionary[key] += value

        new_dict: Dict[int, int] = {}
        for current_key, current_value in outcomes.items():
            total = sum(DropKeepExpression._string_key_to_list(current_key))
            safe_add_to_dict(new_dict, total, current_value)
        return new_dict

    def get_contained_variables(
        self,
    ) -> Set[str]:
        return set()
