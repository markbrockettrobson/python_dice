import abc
import typing

from python_dice.interface.constraint.i_constraint import IConstraint
from python_dice.interface.constraint.i_var_value_constraint import IVarValueConstraint


class IConstraintFactory(abc.ABC):
    @property
    @abc.abstractmethod
    def impossible_constraint(self) -> IConstraint:
        pass

    @property
    @abc.abstractmethod
    def null_constraint(self) -> IConstraint:
        pass

    @abc.abstractmethod
    def var_value_constraint(self, name: str, values: typing.Set[int]) -> IVarValueConstraint:
        pass
