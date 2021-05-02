import operator
import typing

from python_dice.interface.constraint.i_constraint import IConstraint
from python_dice.interface.constraint.i_constraint_merger import IConstraintMerger
from python_dice.interface.constraint.i_constraint_set import IConstraintSet


class ConstraintSet(IConstraintSet):
    def __init__(self, constraints_set: typing.Set[IConstraint], constraint_merger: IConstraintMerger):
        self._constraints_set: typing.Set[IConstraint] = set()
        self._constraint_merger = constraint_merger

        if len(constraints_set) == 0:
            raise ValueError("can not build an empty constraint set. use a null constraint.")
        for constraint in constraints_set:
            self.add_constraint(constraint)

    @property
    def constraints(self) -> typing.Set[IConstraint]:
        return self._constraints_set.copy()

    def add_constraint(self, constraint: IConstraint):
        self._constraints_set = self._constraint_merger.merge_new_constraints(
            constraint_set=self._constraints_set, new_constraint=constraint
        )

    def complies(self, var_values: typing.Dict[str, int]) -> bool:
        for constraint in self._constraints_set:
            if not constraint.complies(var_values=var_values):
                return False
        return True

    def is_possible(self) -> bool:
        for constraint in self._constraints_set:
            if not constraint.is_possible():
                return False
        return True

    def combine_sets(self, constraint_set: IConstraintSet) -> IConstraintSet:
        new_set = self._constraints_set.union(constraint_set.constraints)
        return ConstraintSet(new_set, self._constraint_merger)

    def __eq__(self, other: object) -> bool:
        return str(self) == str(other)

    def __ne__(self, other: object) -> bool:
        return not self == other

    def __str__(self) -> str:
        return f"{ConstraintSet.__name__}: {str(self._constraints_set)}"

    def __repr__(self) -> str:
        return self.__str__()

    def __hash__(self) -> int:
        current_hash = hash(ConstraintSet.__name__)
        for constraint in self._constraints_set:
            current_hash = operator.xor(current_hash, hash(constraint))
        return current_hash
