import typing

from python_dice.interface.constraint.i_constraint import IConstraint
from python_dice.interface.constraint.i_constraint_merger import IConstraintMerger
from python_dice.interface.constraint.i_constraint_set import IConstraintSet


class ConstraintSet(IConstraintSet):
    def __init__(self, constraint_merger: IConstraintMerger):
        self._constraints_set: typing.Set[IConstraint] = set()
        self._constraint_merger = constraint_merger

    def add_constraint(self, constraint: IConstraint):
        self._constraints_set = self._constraint_merger.merge_new_constraints(
            constraint_set=self._constraints_set, new_constraint=constraint
        )

    def complies(self, var_values: typing.Dict[str, int]) -> bool:
        for constraint in self._constraints_set:
            if not constraint.complies(var_values=var_values):
                return False
        return True

    def __eq__(self, other: object) -> bool:
        return str(self) == str(other)

    def __ne__(self, other: object) -> bool:
        return not self == other

    def __str__(self) -> str:
        return f"{ConstraintSet.__name__}: {str(self._constraints_set)}"
