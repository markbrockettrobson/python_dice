import abc

from python_dice.interface.probability_distribution.i_probability_distribution import IProbabilityDistribution


class IProbabilityDistributionState(abc.ABC):
    @abc.abstractmethod
    def get_var(self, name: str) -> IProbabilityDistribution:
        pass

    @abc.abstractmethod
    def has_var(self, name: str) -> bool:
        pass

    @abc.abstractmethod
    def set_var(
        self,
        name: str,
        distribution: IProbabilityDistribution,
    ) -> None:
        pass

    @abc.abstractmethod
    def get_var_dict(self):
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

    @abc.abstractmethod
    def get_constant_dict(self):
        pass
