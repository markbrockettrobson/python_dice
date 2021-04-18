import abc
import typing

from python_dice.interface.constraint.i_constraint import IConstraint


class IConstraintSet(abc.ABC):
    @abc.abstractmethod
    def add_constraint(self, constraint: IConstraint):
        pass

    @abc.abstractmethod
    def complies(self, var_values: typing.Dict[str, int]) -> bool:
        pass

    @abc.abstractmethod
    def __eq__(self, other: object) -> bool:
        pass

    @abc.abstractmethod
    def __ne__(self, other: object) -> bool:
        pass

    @abc.abstractmethod
    def __str__(self) -> str:
        pass
