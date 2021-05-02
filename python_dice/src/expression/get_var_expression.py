from typing import Callable, Set

import rply  # type: ignore

from python_dice.interface.expression.i_dice_expression import IDiceExpression
from python_dice.interface.probability_distribution.i_probability_distribution import IProbabilityDistribution
from python_dice.interface.probability_distribution.i_probability_distribution_factory import (
    IProbabilityDistributionFactory,
)
from python_dice.interface.probability_distribution.i_probability_distribution_state import (
    IProbabilityDistributionState,
)


class GetVarExpression(IDiceExpression):
    TOKEN_RULE = """expression : NAME"""

    @staticmethod
    def add_production_function(
        parser_generator: rply.ParserGenerator, probability_distribution_factory: IProbabilityDistributionFactory
    ) -> Callable:
        @parser_generator.production(GetVarExpression.TOKEN_RULE)
        def get_var(state, tokens) -> IDiceExpression:
            return GetVarExpression(state, tokens[0].value)

        return get_var

    def __init__(self, state: IProbabilityDistributionState, name: str):
        self._state = state
        self._name = name

    def roll(self) -> int:
        return self._state.get_constant(self._name)

    def max(self) -> int:
        return self._state.get_constant(self._name)

    def min(self) -> int:
        return self._state.get_constant(self._name)

    def __str__(self) -> str:
        return f"{self._name}"

    def estimated_cost(self) -> int:
        return self._state.get_constant(self._name)

    def get_probability_distribution(self) -> IProbabilityDistribution:
        return self._state.get_var(self._name)

    def get_contained_variables(
        self,
    ) -> Set[str]:
        return {self._name}
