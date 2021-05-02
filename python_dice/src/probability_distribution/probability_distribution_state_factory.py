import typing

from python_dice.interface.constraint.i_constraint_factory import IConstraintFactory
from python_dice.interface.probability_distribution.i_probability_distribution_factory import (
    IProbabilityDistributionFactory,
)
from python_dice.interface.probability_distribution.i_probability_distribution_state import (
    IProbabilityDistributionState,
)
from python_dice.interface.probability_distribution.i_probability_distribution_state_factory import (
    IProbabilityDistributionStateFactory,
)
from python_dice.src.constraint.constraint_factory import ConstraintFactory
from python_dice.src.probability_distribution.probability_distribution_factory import ProbabilityDistributionFactory
from python_dice.src.probability_distribution.probability_distribution_state import ProbabilityDistributionState


class ProbabilityDistributionStateFactory(IProbabilityDistributionStateFactory):
    def __init__(
        self,
        probability_distribution_factory: typing.Optional[IProbabilityDistributionFactory] = None,
        constraint_factory: typing.Optional[IConstraintFactory] = None,
    ):
        if probability_distribution_factory is None:
            probability_distribution_factory = ProbabilityDistributionFactory()
        if constraint_factory is None:
            constraint_factory = ConstraintFactory()

        self._probability_distribution_factory = probability_distribution_factory
        self._constraint_factory = constraint_factory

    def create_new_empty_set(self) -> IProbabilityDistributionState:
        return ProbabilityDistributionState(
            probability_distribution_factory=self._probability_distribution_factory,
            constraint_factory=self._constraint_factory,
        )
