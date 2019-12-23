import abc
import typing

import PIL.Image as Image

import python_dice.interface.i_probability_distribution as i_probability_distribution


class IPythonDiceInterpreter(abc.ABC):
    @abc.abstractmethod
    def roll(self, input_text: typing.List[str]) -> typing.Dict[str, int]:
        """

        :return: output of state of the pydice program
        """

    @abc.abstractmethod
    def max(self, input_text: typing.List[str]) -> typing.Dict[str, int]:
        """

        :return: output of state of the pydice program
        """

    @abc.abstractmethod
    def min(self, input_text: typing.List[str]) -> typing.Dict[str, int]:
        """

        :return: output of state of the pydice program
        """

    @abc.abstractmethod
    def get_probability_distributions_dict(
        self, input_text: typing.List[str]
    ) -> typing.Dict[str, typing.Dict[int, float]]:
        """

        :return: output of state of the pydice program
        """

    @abc.abstractmethod
    def get_probability_distributions(
        self, input_text: typing.List[str]
    ) -> typing.Dict[str, i_probability_distribution.IProbabilityDistribution]:
        """

        :return: output of state of the pydice program
        """

    @abc.abstractmethod
    def get_histogram(self, input_text: typing.List[str]) -> Image:
        """

        :return: output of state of the pydice program
        """

    @abc.abstractmethod
    def get_at_least_histogram(self, input_text: typing.List[str]) -> Image:
        """

        :return: output of state of the pydice program
        """

    @abc.abstractmethod
    def get_at_most_histogram(self, input_text: typing.List[str]) -> Image:
        """

        :return: output of state of the pydice program
        """

    @abc.abstractmethod
    def get_average(self, input_text: typing.List[str]) -> typing.Dict[str, float]:
        """

        :return: output of state of the pydice program
        """
