from abc import ABC, abstractmethod
from typing import Set

from python_dice.interface.constraint.i_constraint import IConstraint


class IConstraintMerger(ABC):
    @abstractmethod
    def merge_constraints(self, constraint_set: Set[IConstraint]) -> Set[IConstraint]:
        pass

    @abstractmethod
    def merge_new_constraints(self, constraint_set: Set[IConstraint], new_constraint: IConstraint) -> Set[IConstraint]:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def __repr__(self) -> str:
        pass
