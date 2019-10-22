import typing

import python_dice.interface.i_probability_state as i_probability_state
import python_dice.interface.i_python_dice_interpreter as i_python_dice_interpreter
import python_dice.interface.i_python_dice_parser as i_python_dice_parser
import python_dice.src.probability_state as probability_state
import python_dice.src.python_dice_parser as python_dice_parser


class PythonDiceInterpreter(i_python_dice_interpreter.IPythonDiceInterpreter):
    def __init__(
        self,
        parser: i_python_dice_parser.IPythonDiceParser = None,
        starting_state: i_probability_state.IProbabilityDistributionState = None,
    ):
        if parser is None:
            parser = python_dice_parser.PythonDiceParser()
        if starting_state is None:
            starting_state = probability_state.ProbabilityState()
        self._parser = parser
        self._state = starting_state

    def roll(
        self, input_text: typing.List[str]
    ) -> i_probability_state.IProbabilityDistributionState:
        for line in input_text:
            token, _ = self._parser.parse(line, state=self._state)
            token.roll()
        return self._state

    def max(
        self, input_text: typing.List[str]
    ) -> i_probability_state.IProbabilityDistributionState:
        for line in input_text:
            token, _ = self._parser.parse(line, state=self._state)
            token.max()
        return self._state

    def min(
        self, input_text: typing.List[str]
    ) -> i_probability_state.IProbabilityDistributionState:
        for line in input_text:
            token, _ = self._parser.parse(line, state=self._state)
            token.min()
        return self._state

    def get_probability_distribution(
        self, input_text: typing.List[str]
    ) -> i_probability_state.IProbabilityDistributionState:
        for line in input_text:
            token, _ = self._parser.parse(line, state=self._state)
            token.get_probability_distribution()
        return self._state
