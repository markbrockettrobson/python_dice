import typing

import rply

import python_dice.interface.i_probability_distribution as i_probability_distribution
import python_dice.interface.i_probability_state as i_probability_state
import python_dice.interface.python_dice_expression.i_dice_expression as i_dice_expression


class GetVarExpression(i_dice_expression.IDiceExpression):
    TOKEN_RULE = """expression : NAME"""

    @staticmethod
    def add_production_function(
        parser_generator: rply.ParserGenerator,
    ) -> typing.Callable:
        @parser_generator.production(GetVarExpression.TOKEN_RULE)
        def get_var(state, tokens) -> i_dice_expression.IDiceExpression:
            return GetVarExpression(state, tokens[0].value)

        return get_var

    def __init__(
        self, state: i_probability_state.IProbabilityDistributionState, name: str
    ):
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

    def get_probability_distribution(
        self,
    ) -> i_probability_distribution.IProbabilityDistribution:
        return self._state.get_var(self._name)
