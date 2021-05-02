import typing

import rply  # type: ignore

from python_dice.interface.expression.i_dice_expression import IDiceExpression
from python_dice.interface.probability_distribution.i_probability_distribution import IProbabilityDistribution
from python_dice.interface.probability_distribution.i_probability_distribution_factory import (
    IProbabilityDistributionFactory,
)
from python_dice.src.probability_distribution.probability_distribution_state import ProbabilityDistributionState


class VarAssignmentExpression(IDiceExpression):

    TOKEN_RULE = """expression : VAR NAME ASSIGNMENT expression"""

    @staticmethod
    def add_production_function(
        parser_generator: rply.ParserGenerator, probability_distribution_factory: IProbabilityDistributionFactory
    ) -> typing.Callable:
        @parser_generator.production(VarAssignmentExpression.TOKEN_RULE)
        def var_assignment_operation(state, tokens) -> IDiceExpression:
            return VarAssignmentExpression(state, tokens[1].value, tokens[3])

        return var_assignment_operation

    def __init__(
        self,
        state: ProbabilityDistributionState,
        name: str,
        expression: IDiceExpression,
    ):
        self._state = state
        self._name = name
        self._expression = expression

    def roll(self) -> int:
        roll_value = self._expression.roll()
        self._state.set_constant(self._name, roll_value)
        return roll_value

    def max(self) -> int:
        max_value = self._expression.max()
        self._state.set_constant(self._name, max_value)
        self._state.set_var(self._name, self._expression.get_probability_distribution())
        return max_value

    def min(self) -> int:
        min_value = self._expression.min()
        self._state.set_constant(self._name, min_value)
        self._state.set_var(self._name, self._expression.get_probability_distribution())
        return min_value

    def __str__(self) -> str:
        return f"VAR {self._name} = {str(self._expression)}"

    def estimated_cost(self) -> int:
        cost = self._expression.estimated_cost()
        self._state.set_constant(self._name, cost)
        return 2 + cost

    def get_probability_distribution(self) -> IProbabilityDistribution:
        distribution = self._expression.get_probability_distribution()
        self._state.set_var(self._name, distribution)
        return distribution

    def get_contained_variables(
        self,
    ) -> typing.Set[str]:
        return set()
