import pydice.interface.i_dice_statement as i_dice_statement


class ConstantInteger(i_dice_statement.IDiceStatement):
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
