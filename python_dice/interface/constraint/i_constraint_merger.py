from abc import ABC, abstractmethod
import typing

from python_dice.interface.constraint.i_constraint import IConstraint


class IConstraintMerger(ABC):
    @abstractmethod
    def merge_constraints(self, constraint_set: typing.Set[IConstraint]) -> typing.Set[IConstraint]:
        pass

    @abstractmethod
    def merge_new_constraints(
        self, constraint_set: typing.Set[IConstraint], new_constraint: IConstraint
    ) -> typing.Set[IConstraint]:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def __repr__(self) -> str:
        pass
