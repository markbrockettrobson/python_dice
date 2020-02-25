import re
import typing


def get_single_dice_outcome_map(dice_type_string: str) -> typing.Dict[int, int]:
    def save_add(dictionary, value):
        if value not in dictionary:
            dictionary[value] = 0
        dictionary[value] += 1

    if re.match(r"\d+", dice_type_string) is not None:
        value_dictionary = {value: 1 for value in range(1, int(dice_type_string) + 1)}
    elif dice_type_string == "%":
        value_dictionary = {value: 1 for value in range(1, 100 + 1)}
    elif dice_type_string == "F":
        value_dictionary = {-1: 1, 0: 1, 1: 1}
    else:
        number_list = [
            int(value)
            for value in re.split(r",", re.sub(r"(\[|\]|\s+)", "", dice_type_string))
        ]
        value_dictionary = {}
        for number in number_list:
            save_add(value_dictionary, number)
    return value_dictionary
