import typing

from python_dice.interface.constraint.i_constraint import IConstraint
from python_dice.interface.constraint.i_impossible_constraint import IImpossibleConstraint


class ImpossibleConstraint(IImpossibleConstraint):
    def complies(self, var_values: typing.Dict[str, int]) -> bool:
        return True

    def can_merge(self, other: IConstraint) -> bool:
        return True

    def merge(self, other: IConstraint) -> IConstraint:
        return self

    def __eq__(self, other: object) -> bool:
        return str(self) == str(other)

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __str__(self) -> str:
        return f"{ImpossibleConstraint.__name__}"