import abc
import typing

import python_dice.interface.i_probability_distribution as i_probability_distribution


class IProbabilityDistributionState(abc.ABC):
    @abc.abstractmethod
    def get_var(self, name: str) -> i_probability_distribution.IProbabilityDistribution:
        pass

    @abc.abstractmethod
    def has_var(self, name: str) -> bool:
        pass

    @abc.abstractmethod
    def set_var(
        self,
        name: str,
        distribution: i_probability_distribution.IProbabilityDistribution,
    ) -> None:
        pass

    @abc.abstractmethod
    def get_constant(self, name: str) -> int:
        pass

    @abc.abstractmethod
    def has_constant(self, name: str) -> bool:
        pass

    @abc.abstractmethod
    def set_constant(self, name: str, value: int) -> None:
        pass
