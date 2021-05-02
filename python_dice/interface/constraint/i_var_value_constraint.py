import abc
import typing

from python_dice.interface.constraint.i_constraint import IConstraint


class IVarValueConstraint(IConstraint):
    @property
    @abc.abstractmethod
    def name(self) -> str:
        pass

    @property
    @abc.abstractmethod
    def values(self) -> typing.Set[int]:
        pass
