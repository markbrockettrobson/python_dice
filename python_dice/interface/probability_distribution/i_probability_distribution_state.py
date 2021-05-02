from abc import ABC, abstractmethod

from python_dice.interface.probability_distribution.i_probability_distribution import IProbabilityDistribution


class IProbabilityDistributionState(ABC):
    @abstractmethod
    def get_var(self, name: str) -> IProbabilityDistribution:
        pass

    @abstractmethod
    def has_var(self, name: str) -> bool:
        pass

    @abstractmethod
    def set_var(
        self,
        name: str,
        distribution: IProbabilityDistribution,
    ) -> None:
        pass

    @abstractmethod
    def get_var_dict(self):
        pass

    @abstractmethod
    def get_constant(self, name: str) -> int:
        pass

    @abstractmethod
    def has_constant(self, name: str) -> bool:
        pass

    @abstractmethod
    def set_constant(self, name: str, value: int) -> None:
        pass

    @abstractmethod
    def get_constant_dict(self):
        pass
