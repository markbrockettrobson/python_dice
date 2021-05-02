import abc

from python_dice.interface.probability_distribution.i_probability_distribution_state import (
    IProbabilityDistributionState,
)


class IProbabilityDistributionStateFactory(abc.ABC):
    @abc.abstractmethod
    def create_new_empty_set(self) -> IProbabilityDistributionState:
        pass
