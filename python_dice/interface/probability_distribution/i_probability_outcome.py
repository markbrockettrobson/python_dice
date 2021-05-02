from abc import ABC, abstractmethod

from python_dice.interface.constraint.i_constraint_set import IConstraintSet


class IProbabilityOutcome(ABC):
    @property
    @abstractmethod
    def value(self) -> int:
        pass

    @property
    @abstractmethod
    def constraint_set(self) -> IConstraintSet:
        pass

    @abstractmethod
    def is_possible(self) -> bool:
        pass

    @abstractmethod
    def __add__(self, other: object) -> "IProbabilityOutcome":
        pass

    @abstractmethod
    def __sub__(self, other: object) -> "IProbabilityOutcome":
        pass

    @abstractmethod
    def __mul__(self, other: object) -> "IProbabilityOutcome":
        pass

    @abstractmethod
    def __floordiv__(self, other: object) -> "IProbabilityOutcome":
        pass

    @abstractmethod
    def __equal__(self, other: object) -> "IProbabilityOutcome":
        pass

    @abstractmethod
    def __not_equal__(self, other: object) -> "IProbabilityOutcome":
        pass

    @abstractmethod
    def __lt__(self, other: object) -> "IProbabilityOutcome":
        pass

    @abstractmethod
    def __le__(self, other: object) -> "IProbabilityOutcome":
        pass

    @abstractmethod
    def __gt__(self, other: object) -> "IProbabilityOutcome":
        pass

    @abstractmethod
    def __ge__(self, other: object) -> "IProbabilityOutcome":
        pass

    @abstractmethod
    def __and__(self, other: object) -> "IProbabilityOutcome":
        pass

    @abstractmethod
    def __or__(self, other: object) -> "IProbabilityOutcome":
        pass

    @abstractmethod
    def not_operator(self) -> "IProbabilityOutcome":
        pass

    @abstractmethod
    def max_operator(self, other: object) -> "IProbabilityOutcome":
        pass

    @abstractmethod
    def min_operator(self, other: object) -> "IProbabilityOutcome":
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

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        pass

    @abstractmethod
    def __abs__(self) -> "IProbabilityOutcome":
        pass
