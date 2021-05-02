from abc import ABC, abstractmethod
from typing import Dict, List

from PIL import Image  # type: ignore

from python_dice.interface.probability_distribution.i_probability_distribution import IProbabilityDistribution


class IPythonDiceInterpreter(ABC):
    @abstractmethod
    def roll(self, input_text: List[str]) -> Dict[str, int]:
        """

        :return: output of state of the python program
        """

    @abstractmethod
    def max(self, input_text: List[str]) -> Dict[str, int]:
        """

        :return: output of state of the python program
        """

    @abstractmethod
    def min(self, input_text: List[str]) -> Dict[str, int]:
        """

        :return: output of state of the python program
        """

    @abstractmethod
    def get_probability_distributions_dict(self, input_text: List[str]) -> Dict[str, Dict[int, float]]:
        """

        :return: output of state of the python program
        """

    @abstractmethod
    def get_probability_distributions(self, input_text: List[str]) -> Dict[str, IProbabilityDistribution]:
        """

        :return: output of state of the python program
        """

    @abstractmethod
    def get_histogram(self, input_text: List[str]) -> Image:
        """

        :return: output of state of the python program
        """

    @abstractmethod
    def get_at_least_histogram(self, input_text: List[str]) -> Image:
        """

        :return: output of state of the python program
        """

    @abstractmethod
    def get_at_most_histogram(self, input_text: List[str]) -> Image:
        """

        :return: output of state of the python program
        """

    @abstractmethod
    def get_average(self, input_text: List[str]) -> Dict[str, float]:
        """

        :return: output of state of the python program
        """

    @abstractmethod
    def get_estimated_cost(self, input_text: List[str]) -> int:
        """

        :return: total cost estimate for python dice program
        """
