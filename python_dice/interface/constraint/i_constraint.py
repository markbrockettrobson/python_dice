import abc
import typing


class IConstraint(abc.ABC):
    @abc.abstractmethod
    def complies(self, var_values: typing.Dict[str, int]) -> bool:
        pass

    @abc.abstractmethod
    def can_merge(self, other: "IConstraint") -> bool:
        pass

    @abc.abstractmethod
    def merge(self, other: "IConstraint") -> "IConstraint":
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
