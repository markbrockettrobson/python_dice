from typing import Dict, List, Optional

from PIL import Image  # type: ignore

from python_dice.interface.i_python_dice_interpreter import IPythonDiceInterpreter
from python_dice.interface.i_python_dice_parser import IPythonDiceParser
from python_dice.interface.probability_distribution.i_probability_distribution import IProbabilityDistribution
from python_dice.interface.probability_distribution.i_probability_distribution_factory import (
    IProbabilityDistributionFactory,
)
from python_dice.interface.probability_distribution.i_probability_distribution_state import (
    IProbabilityDistributionState,
)
from python_dice.interface.probability_distribution.i_probability_distribution_state_factory import (
    IProbabilityDistributionStateFactory,
)
from python_dice.src.probability_distribution.probability_distribution_factory import ProbabilityDistributionFactory
from python_dice.src.probability_distribution.probability_distribution_state_factory import (
    ProbabilityDistributionStateFactory,
)
from python_dice.src.python_dice_parser import PythonDiceParser


class PythonDiceInterpreter(IPythonDiceInterpreter):
    def __init__(
        self,
        parser: Optional[IPythonDiceParser] = None,
        starting_state: Optional[IProbabilityDistributionState] = None,
        probability_distribution_state_factory: Optional[IProbabilityDistributionStateFactory] = None,
        probability_distribution_factory: Optional[IProbabilityDistributionFactory] = None,
    ):
        if parser is None:
            parser = PythonDiceParser()
        if probability_distribution_state_factory is None:
            probability_distribution_state_factory = ProbabilityDistributionStateFactory()
        if probability_distribution_factory is None:
            probability_distribution_factory = ProbabilityDistributionFactory()
        if starting_state is None:
            starting_state = probability_distribution_state_factory.create_new_empty_set()
        self._parser = parser
        self._state = starting_state
        self._probability_distribution_factory = probability_distribution_factory

    def roll(self, input_text: List[str]) -> Dict[str, int]:
        return_dict = {}
        for line in input_text:
            token, _ = self._parser.parse(line, state=self._state)
            stdout = token.roll()
            return_dict = self._state.get_constant_dict()
            return_dict["stdout"] = stdout
        return return_dict

    def max(self, input_text: List[str]) -> Dict[str, int]:
        return_dict = {}
        for line in input_text:
            token, _ = self._parser.parse(line, state=self._state)
            stdout = token.max()
            return_dict = self._state.get_constant_dict()
            return_dict["stdout"] = stdout
        return return_dict

    def min(self, input_text: List[str]) -> Dict[str, int]:
        return_dict = {}
        for line in input_text:
            token, _ = self._parser.parse(line, state=self._state)
            stdout = token.min()
            return_dict = self._state.get_constant_dict()
            return_dict["stdout"] = stdout
        return return_dict

    def get_probability_distributions_dict(self, input_text: List[str]) -> Dict[str, Dict[int, float]]:
        return_dict = {}
        for line in input_text:
            token, _ = self._parser.parse(line, state=self._state)
            stdout = token.get_probability_distribution()
            return_dict = self._state.get_var_dict()
            return_dict["stdout"] = stdout
        return {key: value.get_dict_form() for key, value in return_dict.items()}

    def get_probability_distributions(self, input_text: List[str]) -> Dict[str, IProbabilityDistribution]:
        return_dict = {}
        for line in input_text:
            token, _ = self._parser.parse(line, state=self._state)
            stdout = token.get_probability_distribution()
            return_dict = self._state.get_var_dict()
            return_dict["stdout"] = stdout
        return {key: return_dict[key] for key in return_dict.keys()}

    def get_average(self, input_text: List[str]) -> Dict[str, float]:
        return_dict = {}
        for line in input_text:
            token, _ = self._parser.parse(line, state=self._state)
            stdout = token.get_probability_distribution()
            return_dict = self._state.get_var_dict()
            return_dict["stdout"] = stdout
        return {key: value.average() for key, value in return_dict.items()}

    def get_histogram(self, input_text: List[str]) -> Image:
        stdout: IProbabilityDistribution = self._probability_distribution_factory.create()
        for line in input_text:
            token, _ = self._parser.parse(line, state=self._state)
            stdout = token.get_probability_distribution()
        return stdout.get_histogram()

    def get_at_least_histogram(self, input_text: List[str]) -> Image:
        stdout: IProbabilityDistribution = self._probability_distribution_factory.create()
        for line in input_text:
            token, _ = self._parser.parse(line, state=self._state)
            stdout = token.get_probability_distribution()
        return stdout.get_at_least_histogram()

    def get_at_most_histogram(self, input_text: List[str]) -> Image:
        stdout: IProbabilityDistribution = self._probability_distribution_factory.create()
        for line in input_text:
            token, _ = self._parser.parse(line, state=self._state)
            stdout = token.get_probability_distribution()
        return stdout.get_at_most_histogram()

    def get_estimated_cost(self, input_text: List[str]) -> int:
        total_cost = 0
        for line in input_text:
            token, _ = self._parser.parse(line, state=self._state)
            line_cost = token.estimated_cost()
            total_cost += line_cost
        return total_cost
