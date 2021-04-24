import abc
import typing

from python_dice.interface.constraint.i_constraint import IConstraint
from python_dice.interface.constraint.i_constraint_merger import IConstraintMerger


class IConstraintSet(abc.ABC):
    @abc.abstractmethod
    def add_constraint(self, constraint: IConstraint):
        pass

    @classmethod
    @abc.abstractmethod
    def build_from_set(
        cls, constraints_set: typing.Set[IConstraint], constraint_merger: IConstraintMerger
    ) -> "IConstraintSet":
        pass

    @property
    @abc.abstractmethod
    def constraints(self) -> typing.Set[IConstraint]:
        pass

    @abc.abstractmethod
    def complies(self, var_values: typing.Dict[str, int]) -> bool:
        pass

    @abc.abstractmethod
    def combine_sets(self, constraint_set: "IConstraintSet") -> "IConstraintSet":
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

    @abc.abstractmethod
    def __repr__(self) -> str:
        pass
