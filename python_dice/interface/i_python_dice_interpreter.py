import abc
import typing

import python_dice.interface.i_probability_state as i_probability_state


class IPythonDiceInterpreter(abc.ABC):
    @abc.abstractmethod
    def roll(
        self, input_text: typing.List[str]
    ) -> i_probability_state.IProbabilityDistributionState:
        """

        :return: output of state of the pydice program
        """

    @abc.abstractmethod
    def max(
        self, input_text: typing.List[str]
    ) -> i_probability_state.IProbabilityDistributionState:
        """

        :return: output of state of the pydice program
        """

    @abc.abstractmethod
    def min(
        self, input_text: typing.List[str]
    ) -> i_probability_state.IProbabilityDistributionState:
        """

        :return: output of state of the pydice program
        """

    @abc.abstractmethod
    def get_probability_distribution(
        self, input_text: typing.List[str]
    ) -> i_probability_state.IProbabilityDistributionState:
        """

        :return: output of state of the pydice program
        """
