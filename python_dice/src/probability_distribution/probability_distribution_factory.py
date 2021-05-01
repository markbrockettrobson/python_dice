import typing

from python_dice.interface.probability_distribution.i_probability_distribution import IProbabilityDistribution
from python_dice.interface.probability_distribution.i_probability_distribution_factory import (
    IProbabilityDistributionFactory,
)
from python_dice.interface.probability_distribution.i_probability_outcome import IProbabilityOutcome
from python_dice.interface.probability_distribution.i_probability_outcome_factory import IProbabilityOutcomeFactory
from python_dice.src.probability_distribution.probability_distribution import ProbabilityDistribution
from python_dice.src.probability_distribution.probability_outcome_factory import ProbabilityOutcomeFactory


class ProbabilityDistributionFactory(IProbabilityDistributionFactory):
    def __init__(self, probability_outcome_factory: typing.Optional[IProbabilityOutcomeFactory] = None):
        if probability_outcome_factory is None:
            probability_outcome_factory = ProbabilityOutcomeFactory()
        self._probability_outcome_factory = probability_outcome_factory

    def create(
        self,
        result_map: typing.Optional[typing.Union[typing.Dict[IProbabilityOutcome, int], typing.Dict[int, int]]] = None,
    ) -> IProbabilityDistribution:
        return ProbabilityDistribution(self._probability_outcome_factory, result_map)
