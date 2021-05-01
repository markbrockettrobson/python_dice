import abc
import typing

from python_dice.interface.probability_distribution.i_probability_distribution import IProbabilityDistribution
from python_dice.interface.probability_distribution.i_probability_outcome import IProbabilityOutcome


class IProbabilityDistributionFactory(abc.ABC):
    @abc.abstractmethod
    def create(
        self,
        result_map: typing.Optional[typing.Union[typing.Dict[IProbabilityOutcome, int], typing.Dict[int, int]]] = None,
    ) -> IProbabilityDistribution:
        pass
