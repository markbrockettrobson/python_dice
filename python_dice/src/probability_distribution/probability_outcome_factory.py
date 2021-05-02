from typing import Optional

from python_dice.interface.constraint.i_constraint_set_factory import IConstraintSetFactory
from python_dice.interface.probability_distribution.i_probability_outcome import IProbabilityOutcome
from python_dice.interface.probability_distribution.i_probability_outcome_factory import IProbabilityOutcomeFactory
from python_dice.src.constraint.constraint_set_factory import ConstraintSetFactory
from python_dice.src.probability_distribution.probability_outcome import ProbabilityOutcome


class ProbabilityOutcomeFactory(IProbabilityOutcomeFactory):
    def __init__(self, constraint_set_factory: Optional[IConstraintSetFactory] = None):
        if constraint_set_factory is None:
            constraint_set_factory = ConstraintSetFactory()
        self._constraint_set_factory = constraint_set_factory

    def create_empty(self, value: int) -> IProbabilityOutcome:
        return ProbabilityOutcome(value, self._constraint_set_factory.create_constraint_set())
