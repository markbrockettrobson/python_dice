import abc

from python_dice.interface.probability_distribution.i_probability_outcome import IProbabilityOutcome


class IProbabilityOutcomeFactory(abc.ABC):
    @abc.abstractmethod
    def create_empty(self, value: int) -> IProbabilityOutcome:
        pass
