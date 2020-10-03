import typing

import rply

import python_dice.interface.i_probability_distribution as i_probability_distribution
import python_dice.interface.python_dice_expression.i_dice_expression as i_dice_expression


class ParenthesisEnclosedExpression(i_dice_expression.IDiceExpression):
    RULE = """expression : OPEN_PARENTHESIS expression CLOSE_PARENTHESIS"""

    @staticmethod
    def add_production_function(
        parser_generator: rply.ParserGenerator,
    ) -> typing.Callable:
        @parser_generator.production(ParenthesisEnclosedExpression.RULE)
        def parenthesis_enclosed(_, tokens) -> i_dice_expression.IDiceExpression:
            return ParenthesisEnclosedExpression(tokens[1])

        return parenthesis_enclosed

    def __init__(self, expression: i_dice_expression.IDiceExpression):
        self._expression = expression

    def roll(self) -> int:
        return self._expression.roll()

    def max(self) -> int:
        return self._expression.max()

    def min(self) -> int:
        return self._expression.min()

    def __str__(self) -> str:
        return f"({str(self._expression)})"

    def estimated_cost(self) -> int:
        return self._expression.estimated_cost()

    def get_probability_distribution(
        self,
    ) -> i_probability_distribution.IProbabilityDistribution:
        return self._expression.get_probability_distribution()
