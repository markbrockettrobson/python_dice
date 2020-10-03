import typing

import rply

import python_dice.interface.i_probability_distribution as i_probability_distribution
import python_dice.interface.python_dice_expression.i_dice_expression as i_dice_expression
import python_dice.src.probability_state as probability_state


class VarAssignmentExpression(i_dice_expression.IDiceExpression):

    TOKEN_RULE = """expression : VAR NAME ASSIGNMENT expression"""

    @staticmethod
    def add_production_function(
        parser_generator: rply.ParserGenerator,
    ) -> typing.Callable:
        @parser_generator.production(VarAssignmentExpression.TOKEN_RULE)
        def var_assignment_operation(
            state, tokens
        ) -> i_dice_expression.IDiceExpression:
            return VarAssignmentExpression(state, tokens[1].value, tokens[3])

        return var_assignment_operation

    def __init__(
        self,
        state: probability_state.ProbabilityState,
        name: str,
        expression: i_dice_expression.IDiceExpression,
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
        return cost

    def get_probability_distribution(
        self,
    ) -> i_probability_distribution.IProbabilityDistribution:
        distribution = self._expression.get_probability_distribution()
        self._state.set_var(self._name, distribution)
        return distribution
