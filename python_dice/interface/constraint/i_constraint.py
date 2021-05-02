from abc import ABC, abstractmethod
from typing import Dict


class IConstraint(ABC):
    @abstractmethod
    def complies(self, var_values: Dict[str, int]) -> bool:
        pass

    @abstractmethod
    def can_merge(self, other: "IConstraint") -> bool:
        pass

    @abstractmethod
    def merge(self, other: "IConstraint") -> "IConstraint":
        pass

    @abstractmethod
    def is_possible(self) -> bool:
        pass

    @abstractmethod
    def __hash__(self) -> int:
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
