import typing
from abc import abstractmethod

from python_dice.interface.constraint.i_constraint import IConstraint


class IVarValueConstraint(IConstraint):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def values(self) -> typing.Set[int]:
        pass
