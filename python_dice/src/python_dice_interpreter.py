import typing

import PIL.Image as Image

import python_dice.interface.i_probability_distribution as i_probability_distribution
import python_dice.interface.i_probability_state as i_probability_state
import python_dice.interface.i_python_dice_interpreter as i_python_dice_interpreter
import python_dice.interface.i_python_dice_parser as i_python_dice_parser
import python_dice.src.probability_distribution as probability_distribution
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

    def roll(self, input_text: typing.List[str]) -> typing.Dict[str, int]:
        return_dict = {}
        for line in input_text:
            token, _ = self._parser.parse(line, state=self._state)
            stdout = token.roll()
            return_dict = self._state.get_constant_dict()
            return_dict["stdout"] = stdout
        return return_dict

    def max(self, input_text: typing.List[str]) -> typing.Dict[str, int]:
        return_dict = {}
        for line in input_text:
            token, _ = self._parser.parse(line, state=self._state)
            stdout = token.max()
            return_dict = self._state.get_constant_dict()
            return_dict["stdout"] = stdout
        return return_dict

    def min(self, input_text: typing.List[str]) -> typing.Dict[str, int]:
        return_dict = {}
        for line in input_text:
            token, _ = self._parser.parse(line, state=self._state)
            stdout = token.min()
            return_dict = self._state.get_constant_dict()
            return_dict["stdout"] = stdout
        return return_dict

    def get_probability_distributions_dict(
        self, input_text: typing.List[str]
    ) -> typing.Dict[str, typing.Dict[int, float]]:
        return_dict = {}
        for line in input_text:
            token, _ = self._parser.parse(line, state=self._state)
            stdout = token.get_probability_distribution()
            return_dict = self._state.get_var_dict()
            return_dict["stdout"] = stdout
        return {key: value.get_dict_form() for key, value in return_dict.items()}

    def get_probability_distributions(
        self, input_text: typing.List[str]
    ) -> typing.Dict[str, i_probability_distribution.IProbabilityDistribution]:
        return_dict = {}
        for line in input_text:
            token, _ = self._parser.parse(line, state=self._state)
            stdout = token.get_probability_distribution()
            return_dict = self._state.get_var_dict()
            return_dict["stdout"] = stdout
        return {key: return_dict[key] for key in return_dict.keys()}

    def get_average(self, input_text: typing.List[str]) -> typing.Dict[str, float]:
        return_dict = {}
        for line in input_text:
            token, _ = self._parser.parse(line, state=self._state)
            stdout = token.get_probability_distribution()
            return_dict = self._state.get_var_dict()
            return_dict["stdout"] = stdout
        return {key: value.average() for key, value in return_dict.items()}

    def get_histogram(self, input_text: typing.List[str]) -> Image:
        stdout = probability_distribution.ProbabilityDistribution()
        for line in input_text:
            token, _ = self._parser.parse(line, state=self._state)
            stdout = token.get_probability_distribution()
        return stdout.get_histogram()

    def get_at_least_histogram(self, input_text: typing.List[str]) -> Image:
        stdout = probability_distribution.ProbabilityDistribution()
        for line in input_text:
            token, _ = self._parser.parse(line, state=self._state)
            stdout = token.get_probability_distribution()
        return stdout.get_at_least_histogram()

    def get_at_most_histogram(self, input_text: typing.List[str]) -> Image:
        stdout = probability_distribution.ProbabilityDistribution()
        for line in input_text:
            token, _ = self._parser.parse(line, state=self._state)
            stdout = token.get_probability_distribution()
        return stdout.get_at_most_histogram()
