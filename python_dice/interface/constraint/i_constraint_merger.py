import abc
import typing

from python_dice.interface.constraint.i_constraint import IConstraint


class IConstraintMerger(abc.ABC):
    @abc.abstractmethod
    def merge_constraints(self, constraint_set: typing.Set[IConstraint]) -> typing.Set[IConstraint]:
        pass

    @abc.abstractmethod
    def merge_new_constraints(
        self, constraint_set: typing.Set[IConstraint], new_constraint: IConstraint
    ) -> typing.Set[IConstraint]:
        pass

    @abc.abstractmethod
    def __str__(self) -> str:
        pass

    @abc.abstractmethod
    def __repr__(self) -> str:
        pass
