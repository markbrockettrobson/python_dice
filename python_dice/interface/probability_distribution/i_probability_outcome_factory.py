from abc import ABC, abstractmethod

from python_dice.interface.probability_distribution.i_probability_outcome import IProbabilityOutcome


class IProbabilityOutcomeFactory(ABC):
    @abstractmethod
    def create_empty(self, value: int) -> IProbabilityOutcome:
        pass
