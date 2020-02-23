import typing

import numpy
import rply
import re

import python_dice.interface.i_probability_distribution as i_probability_distribution
import python_dice.interface.python_dice_expression.i_dice_expression as i_dice_expression
import python_dice.src.probability_distribution as probability_distribution
import python_dice.src.python_dice_expression.dice_expression as dice_expression
import python_dice.src.python_dice_expression.constant_integer_expression as constant_integer_expression


class DropKeepExpression(i_dice_expression.IDiceExpression):
    TOKEN_RULE = """expression : DROP_KEEP_DICE"""

    @staticmethod
    def add_production_function(
        parser_generator: rply.ParserGenerator
    ) -> typing.Callable:
        @parser_generator.production(DropKeepExpression.TOKEN_RULE)
        def drop_keep(_, tokens) -> i_dice_expression.IDiceExpression:
            return DropKeepExpression(tokens[0].value)
        return drop_keep

    def __init__(self, string_form: str):
        self._string_form = string_form
        self._number_of_dice = self._get_number_of_dice()
        self._number_of_sides = self._get_number_of_sides()
        self._number_to_keep_or_drop = self._get_number_to_keep_or_drop()
        self._simplified_form = None
        if self._is_keep():
            if self._number_of_dice <= self._number_to_keep_or_drop:
                self._simplified_form = dice_expression.DiceExpression(
                    "%dd%d" % (self._number_of_dice, self._number_of_sides)
                )
            elif self._number_to_keep_or_drop == 0:
                self._simplified_form = constant_integer_expression.ConstantIntegerExpression("0")
        else:
            if self._number_of_dice <= self._number_to_keep_or_drop:
                self._simplified_form = constant_integer_expression.ConstantIntegerExpression("0")
            elif self._number_to_keep_or_drop == 0:
                self._simplified_form = dice_expression.DiceExpression(
                    "%dd%d" % (self._number_of_dice, self._number_of_sides)
                )

    def _get_number_of_dice(self) -> int:
        return int(re.split(r"[dk]", self._string_form)[0])

    def _get_number_of_sides(self) -> int:
        return int(re.split(r"[dk]", self._string_form)[1])

    def _get_number_to_keep_or_drop(self) -> int:
        return int(re.split(r"[dk]", self._string_form)[2])

    def _is_keep(self) -> bool:
        return re.split(r"\d+", self._string_form)[2] == 'k'

    def roll(self) -> int:
        dice_rolls = numpy.random.randint(
            1,
            self._number_of_sides + 1,
            self._number_of_dice
        )
        if self._simplified_form is not None:
            return self._simplified_form.roll()

        dice_rolls.sort()
        if self._is_keep():
            return sum(
                dice_rolls[-self._number_to_keep_or_drop:]
            )
        else:
            return sum(
                dice_rolls[:self._number_of_dice - self._number_to_keep_or_drop]
            )

    def max(self) -> int:
        if self._simplified_form is not None:
            return self._simplified_form.max()

        if self._is_keep():
            return self._number_to_keep_or_drop * self._number_of_sides
        else:
            return (self._number_of_dice - self._number_to_keep_or_drop) * self._number_of_sides

    def min(self) -> int:
        if self._simplified_form is not None:
            return self._simplified_form.min()

        if self._is_keep():
            return self._number_to_keep_or_drop
        else:
            return self._number_of_dice - self._number_to_keep_or_drop

    def __str__(self) -> str:
        return f"{self._string_form}"

    def get_probability_distribution(
        self
    ) -> i_probability_distribution.IProbabilityDistribution:
        if self._simplified_form is not None:
            return self._simplified_form.get_probability_distribution()

        is_keep = self._is_keep()
        number_of_sides = self._number_of_sides
        number_of_dice_to_select = self._number_of_dice - self._number_to_keep_or_drop
        number_of_dice_remaining = self._number_to_keep_or_drop
        if is_keep:
            number_of_dice_to_select = self._number_to_keep_or_drop
            number_of_dice_remaining = self._number_of_dice - self._number_to_keep_or_drop

        current = DropKeepExpression._build_dice_dict(
            number_of_dice_to_select,
            number_of_sides
        )
        current = DropKeepExpression._compute_iterations(
            current,
            number_of_dice_remaining,
            number_of_sides,
            is_keep
        )

        out_come_map = DropKeepExpression._collapse_outcomes(current)
        return probability_distribution.ProbabilityDistribution(out_come_map)

    @staticmethod
    def _build_dice_dict(number_of_dice: int, number_of_sides: int) -> typing.Dict[str, int]:
        def safe_add_to_dict(dictionary: typing.Dict[str, int], key: str, value: int) -> None:
            if key not in dictionary:
                dictionary[key] = 0
            dictionary[key] += value

        current_dict = {"": 1}
        for _ in range(number_of_dice):
            new_dict = {}
            for i in range(1, number_of_sides + 1):
                for old_key, old_value in current_dict.items():
                    new_key = DropKeepExpression._string_key_to_list(old_key)
                    new_key.append(i)
                    safe_add_to_dict(
                        new_dict,
                        DropKeepExpression._int_list_to_string(new_key),
                        old_value
                    )
            current_dict = new_dict
        return current_dict

    @staticmethod
    def _string_key_to_list(string: str) -> typing.List[int]:
        if string is "":
            return []
        return [int(n) for n in string.split("-")]

    @staticmethod
    def _int_list_to_string(values: typing.List[int]) -> str:
        values.sort()
        return "-".join([str(n) for n in values])

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
            current: typing.Dict[str, int],
            number_of_dice: int,
            number_of_sides: int,
            is_keep: bool,
    ) -> typing.Dict[str, int]:
        def safe_add_to_dict(dictionary: typing.Dict[str, int], key: str, value: int) -> None:
            if key not in dictionary:
                dictionary[key] = 0
            dictionary[key] += value

        current_dict = current
        for _ in range(number_of_dice):
            new_dict = {}
            for i in range(1, number_of_sides + 1):
                for old_key, old_value in current_dict.items():
                    new_key = DropKeepExpression._update_key_list(old_key, i, is_keep)
                    safe_add_to_dict(new_dict, new_key, old_value)
            current_dict = new_dict
        return current_dict

    @staticmethod
    def _collapse_outcomes(outcomes: typing.Dict[str, int]) -> typing.Dict[int, int]:
        def safe_add_to_dict(dictionary: typing.Dict[int, int], key: int, value: int) -> None:
            if key not in dictionary:
                dictionary[key] = 0
            dictionary[key] += value

        new_dict = {}
        for current_key, current_value in outcomes.items():
            total = sum(DropKeepExpression._string_key_to_list(current_key))
            safe_add_to_dict(new_dict, total, current_value)
        return new_dict
