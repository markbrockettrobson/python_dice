import python_dice.interface.dice_statement.i_dice_statement as i_dice_statement


class ConstantInteger(i_dice_statement.IDiceSyntax):
    TOKEN_NAME = "CONSTANT_INTEGER"
    TOKEN_REGEX = r"-?\d+"

    @staticmethod
    def get_token_name() -> str:
        return ConstantInteger.TOKEN_NAME

    @staticmethod
    def get_token_regex() -> str:
        return ConstantInteger.TOKEN_REGEX

    def __init__(self, number: int):
        self._number = number

    def roll(self) -> int:
        return self._number

    def max(self) -> int:
        return self._number

    def min(self) -> int:
        return self._number

    def __str__(self) -> str:
        return str(self._number)
