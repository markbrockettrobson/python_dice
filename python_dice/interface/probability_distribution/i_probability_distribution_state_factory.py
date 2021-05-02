from abc import ABC, abstractmethod

from python_dice.interface.probability_distribution.i_probability_distribution_state import (
    IProbabilityDistributionState,
)


class IProbabilityDistributionStateFactory(ABC):
    @abstractmethod
    def create_new_empty_set(self) -> IProbabilityDistributionState:
        pass
