import abc
import typing

import PIL.Image as Image


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
    def get_probability_distribution(
        self, input_text: typing.List[str]
    ) -> typing.Dict[str, typing.Dict[int, float]]:
        """

        :return: output of state of the pydice program
        """

    @abc.abstractmethod
    def get_histogram(self, input_text: typing.List[str]) -> Image:
        """

        :return: output of state of the pydice program
        """
