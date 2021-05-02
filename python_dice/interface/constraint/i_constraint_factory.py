from abc import ABC, abstractmethod
import typing

from python_dice.interface.constraint.i_constraint import IConstraint
from python_dice.interface.constraint.i_var_value_constraint import IVarValueConstraint


class IConstraintFactory(ABC):
    @property
    @abstractmethod
    def impossible_constraint(self) -> IConstraint:
        pass

    @property
    @abstractmethod
    def null_constraint(self) -> IConstraint:
        pass

    @abstractmethod
    def var_value_constraint(self, name: str, values: typing.Set[int]) -> IVarValueConstraint:
        pass
