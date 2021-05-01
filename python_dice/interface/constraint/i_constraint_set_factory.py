import abc

from python_dice.interface.constraint.i_constraint_set import IConstraintSet


class IConstraintSetFactory(abc.ABC):
    @abc.abstractmethod
    def create_constraint_set(self) -> IConstraintSet:
        pass
