import abc
from typing import SupportsAbs

from python_dice.interface.constraint.i_constraint_set import IConstraintSet


class IProbabilityOutcome(abc.ABC, SupportsAbs):
    @property
    @abc.abstractmethod
    def value(self) -> int:
        pass

    @property
    @abc.abstractmethod
    def constraint_set(self) -> IConstraintSet:
        pass

    @abc.abstractmethod
    def __add__(self, other: object) -> "IProbabilityOutcome":
        pass

    @abc.abstractmethod
    def __sub__(self, other: object) -> "IProbabilityOutcome":
        pass

    @abc.abstractmethod
    def __mul__(self, other: object) -> "IProbabilityOutcome":
        pass

    @abc.abstractmethod
    def __floordiv__(self, other: object) -> "IProbabilityOutcome":
        pass

    @abc.abstractmethod
    def __equal__(self, other: object) -> "IProbabilityOutcome":
        pass

    @abc.abstractmethod
    def __not_equal__(self, other: object) -> "IProbabilityOutcome":
        pass

    @abc.abstractmethod
    def __lt__(self, other: object) -> "IProbabilityOutcome":
        pass

    @abc.abstractmethod
    def __le__(self, other: object) -> "IProbabilityOutcome":
        pass

    @abc.abstractmethod
    def __gt__(self, other: object) -> "IProbabilityOutcome":
        pass

    @abc.abstractmethod
    def __ge__(self, other: object) -> "IProbabilityOutcome":
        pass

    @abc.abstractmethod
    def __and__(self, other: object) -> "IProbabilityOutcome":
        pass

    @abc.abstractmethod
    def __or__(self, other: object) -> "IProbabilityOutcome":
        pass

    @abc.abstractmethod
    def not_operator(self) -> "IProbabilityOutcome":
        pass

    @abc.abstractmethod
    def max_operator(self, other: object) -> "IProbabilityOutcome":
        pass

    @abc.abstractmethod
    def min_operator(self, other: object) -> "IProbabilityOutcome":
        pass

    @abc.abstractmethod
    def __str__(self) -> str:
        pass

    @abc.abstractmethod
    def __repr__(self) -> str:
        pass
