from typing import Dict

from python_dice.interface.constraint.i_constraint import IConstraint
from python_dice.interface.constraint.i_null_constraint import INullConstraint


class NullConstraint(INullConstraint):
    def complies(self, var_values: Dict[str, int]) -> bool:
        return True

    def can_merge(self, other: IConstraint) -> bool:
        return True

    def is_possible(self) -> bool:
        return True

    def merge(self, other: IConstraint) -> IConstraint:
        return other

    def __hash__(self) -> int:
        return hash(self.__str__())

    def __eq__(self, other: object) -> bool:
        return str(self) == str(other)

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __str__(self) -> str:
        return f"{NullConstraint.__name__}"

    def __repr__(self) -> str:
        return self.__str__()
