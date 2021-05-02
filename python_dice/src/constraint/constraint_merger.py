import typing

from python_dice.interface.constraint.i_constraint import IConstraint
from python_dice.interface.constraint.i_constraint_merger import IConstraintMerger


class ConstraintMerger(IConstraintMerger):
    def merge_constraints(self, constraint_set: typing.Set[IConstraint]) -> typing.Set[IConstraint]:
        return ConstraintMerger.__merge_new_constraints(constraint_set, set())

    def merge_new_constraints(
        self, constraint_set: typing.Set[IConstraint], new_constraint: IConstraint
    ) -> typing.Set[IConstraint]:
        return ConstraintMerger.__merge_new_constraints({new_constraint}, constraint_set)

    @staticmethod
    def __merge_new_constraints(
        new_constraints: typing.Set[IConstraint], constraint_set: typing.Set[IConstraint]
    ) -> typing.Set[IConstraint]:
        values_to_merge = list(new_constraints.copy())
        clean_constraint_set = constraint_set.copy()

        while values_to_merge:
            current_value = values_to_merge.pop()

            new_unclean_values, new_clean_values = ConstraintMerger.__merge_new_constraint(
                current_value, clean_constraint_set
            )
            values_to_merge.extend(new_unclean_values)
            clean_constraint_set = new_clean_values

        return clean_constraint_set

    @staticmethod
    def __merge_new_constraint(
        new_constraint: IConstraint, constraint_set: typing.Set[IConstraint]
    ) -> typing.Tuple[typing.Set[IConstraint], typing.Set[IConstraint]]:
        for constraint in constraint_set:

            if constraint.can_merge(new_constraint):
                unchanged_constraint_set = constraint_set.copy()
                unchanged_constraint_set.remove(constraint)
                changed_constraint_set = {constraint.merge(new_constraint)}
                return changed_constraint_set, unchanged_constraint_set

            if new_constraint.can_merge(constraint):
                unchanged_constraint_set = constraint_set.copy()
                changed_constraint_set = {new_constraint.merge(constraint)}
                unchanged_constraint_set.remove(constraint)
                return changed_constraint_set, unchanged_constraint_set

        constraint_set.add(new_constraint)
        return set(), constraint_set

    def __str__(self) -> str:
        return f"{ConstraintMerger.__name__}"

    def __repr__(self) -> str:
        return self.__str__()
