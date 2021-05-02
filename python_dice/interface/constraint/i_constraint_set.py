from abc import ABC, abstractmethod
import typing

from python_dice.interface.constraint.i_constraint import IConstraint


class IConstraintSet(ABC):
    @abstractmethod
    def add_constraint(self, constraint: IConstraint):
        pass

    @property
    @abstractmethod
    def constraints(self) -> typing.Set[IConstraint]:
        pass

    @abstractmethod
    def complies(self, var_values: typing.Dict[str, int]) -> bool:
        pass

    @abstractmethod
    def is_possible(self) -> bool:
        pass

    @abstractmethod
    def combine_sets(self, constraint_set: "IConstraintSet") -> "IConstraintSet":
        pass

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        pass

    @abstractmethod
    def __ne__(self, other: object) -> bool:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def __repr__(self) -> str:
        pass

    @abstractmethod
    def __hash__(self) -> int:
        pass
