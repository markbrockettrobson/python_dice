
_NUMBER_OF_DICE = r"\d*"
_DICE_SYMBOL = r"d"
_DICE_TYPE = r"(\d+|%|F|\[(\s*(-?)\d+\s*,\s*)*(-?)\d+\s*(,?)\s*])"
_DROP_KEEP = r"[kd]\d+"

DICE_SYNTAX = _NUMBER_OF_DICE + _DICE_SYMBOL + _DICE_TYPE
DROP_KEEP_DICE_SYNTAX = DICE_SYNTAX + _DROP_KEEP
