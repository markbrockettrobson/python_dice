import abc
import typing

import matplotlib.pyplot as pyplot


class IProbabilityDistribution(abc.ABC):
    @abc.abstractmethod
    def get_dict_form(self) -> typing.Dict[int, float]:
        """

        :return: a dict mapping an outcome of the program to a probability of that outcome
                <typing.Dict[int, float]>
        """

    @abc.abstractmethod
    def get_result_map(self) -> typing.Dict[int, int]:
        """

        :return: a dict mapping an outcome of the program to the number of ways to achieve that outcome
                 <typing.Dict[int, int]>
        """

    @abc.abstractmethod
    def show_histogram(self) -> pyplot.Figure:
        """

        prints a plot of the distribution with matplotlib
        :returns the pyplot figure for plot
                 <pyplot.Figure>
        """

    @abc.abstractmethod
    def max(self) -> int:
        """

        :returns: the max roll that could be made
                  <int>
        """

    @abc.abstractmethod
    def min(self) -> int:
        """

        :returns: the min roll that could be made
                  <int>
        """

    @abc.abstractmethod
    def contains_zero(self) -> bool:
        """

        :returns: returns true if the distribution contains zero
                  <bool>
        """

    @abc.abstractmethod
    def __add__(self, other: "IProbabilityDistribution") -> "IProbabilityDistribution":
        pass

    @abc.abstractmethod
    def __sub__(self, other: "IProbabilityDistribution") -> "IProbabilityDistribution":
        pass

    @abc.abstractmethod
    def __mul__(self, other: "IProbabilityDistribution") -> "IProbabilityDistribution":
        pass

    @abc.abstractmethod
    def __floordiv__(
        self, other: "IProbabilityDistribution"
    ) -> "IProbabilityDistribution":
        pass

    @abc.abstractmethod
    def __eq__(self, other: "IProbabilityDistribution") -> "IProbabilityDistribution":
        pass

    @abc.abstractmethod
    def __ne__(self, other: "IProbabilityDistribution") -> "IProbabilityDistribution":
        pass

    @abc.abstractmethod
    def __lt__(self, other: "IProbabilityDistribution") -> "IProbabilityDistribution":
        pass

    @abc.abstractmethod
    def __le__(self, other: "IProbabilityDistribution") -> "IProbabilityDistribution":
        pass

    @abc.abstractmethod
    def __gt__(self, other: "IProbabilityDistribution") -> "IProbabilityDistribution":
        pass

    @abc.abstractmethod
    def __ge__(self, other: "IProbabilityDistribution") -> "IProbabilityDistribution":
        pass

    @abc.abstractmethod
    def __and__(self, other: "IProbabilityDistribution") -> "IProbabilityDistribution":
        pass

    @abc.abstractmethod
    def __or__(self, other: "IProbabilityDistribution") -> "IProbabilityDistribution":
        pass

    @abc.abstractmethod
    def not_operator(self) -> "IProbabilityDistribution":
        pass

    @abc.abstractmethod
    def max_operator(
        self, other: "IProbabilityDistribution"
    ) -> "IProbabilityDistribution":
        pass

    @abc.abstractmethod
    def min_operator(
        self, other: "IProbabilityDistribution"
    ) -> "IProbabilityDistribution":
        pass

    @abc.abstractmethod
    def abs_operator(self) -> "IProbabilityDistribution":
        pass
