import re
from typing import Dict, Iterable


def _find_range(value: str) -> range:
    split_range = re.split("-", value)
    range_start: int
    range_end: int

    if re.match(r"\d+--?\d+", value) is not None:
        range_start = int(split_range[0])
    else:
        range_start = -int(split_range[1])
    if re.match(r"-?\d+--\d+", value) is not None:
        range_end = -int(split_range[-1])
    else:
        range_end = int(split_range[-1])
    return range(min(range_start, range_end), max(range_start, range_end) + 1)


def get_single_dice_outcome_map(dice_type_string: str) -> Dict[int, int]:
    range_values: Iterable

    def safe_add(dictionary, value, amount):
        if value not in dictionary:
            dictionary[value] = 0
        dictionary[value] += amount

    if re.match(r"\d+", dice_type_string) is not None:
        value_dictionary = {value: 1 for value in range(1, int(dice_type_string) + 1)}
    elif dice_type_string == "%":
        value_dictionary = {value: 1 for value in range(1, 100 + 1)}
    elif dice_type_string == "F":
        value_dictionary = {-1: 1, 0: 1, 1: 1}
    else:
        value_dictionary = {}
        for value in re.split(r",", re.sub(r"(\[|\]|\s+)", "", dice_type_string)):
            multiplier = "1"
            if re.match(r"(-?\d+--?\d+|-?\d+)\*\d+", value) is not None:
                value, multiplier = re.split(r"\*", value)
            if re.match(r"-?\d+--?\d+", value) is not None:
                range_values = _find_range(value)
            else:
                range_values = [int(value)]
            for key in range_values:
                safe_add(value_dictionary, key, int(multiplier))
    return value_dictionary
