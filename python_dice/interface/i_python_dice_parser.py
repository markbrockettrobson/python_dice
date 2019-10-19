import abc
import typing

import python_dice.interface.i_probability_state as i_probability_state
import python_dice.interface.python_dice_expression.i_dice_expression as i_dice_expression


class IPythonDiceParser(abc.ABC):
    @abc.abstractmethod
    def parse(
        self,
        input_text: str,
        state: i_probability_state.IProbabilityDistributionState = None,
    ) -> typing.Tuple[
        i_dice_expression.IDiceExpression,
        i_probability_state.IProbabilityDistributionState,
    ]:
        """

        :return: output of pydice program
        """
