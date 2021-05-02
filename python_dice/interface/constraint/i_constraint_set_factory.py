from abc import ABC, abstractmethod

from python_dice.interface.constraint.i_constraint_set import IConstraintSet


class IConstraintSetFactory(ABC):
    @abstractmethod
    def create_constraint_set(self) -> IConstraintSet:
        pass
