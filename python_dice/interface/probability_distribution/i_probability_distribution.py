import abc
import typing

from PIL import Image  # type: ignore

from python_dice.interface.probability_distribution.i_probability_outcome import IProbabilityOutcome


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

    def get_constraint_result_map(self) -> typing.Dict[IProbabilityOutcome, int]:
        """

        :return: a dict mapping an outcome of the program to the number of ways to achieve that outcome
                 <typing.Dict[IProbabilityOutcome, int]>
        """

    @abc.abstractmethod
    def get_histogram(self) -> Image:
        """

        prints a plot of the distribution with matplotlib
        :returns the pyplot figure for plot
                 <Image>
        """

    @abc.abstractmethod
    def get_at_least_histogram(self) -> Image:
        """

        prints a plot of the area under the distribution with matplotlib
        :returns the pyplot figure for plot
                 <Image>
        """

    @abc.abstractmethod
    def get_at_most_histogram(self) -> Image:
        """

        prints a plot of 1 - the area under the distribution with matplotlib
        :returns the pyplot figure for plot
                 <Image>
        """

    @abc.abstractmethod
    def get_compare_histogram(self, other_probability: "IProbabilityDistribution") -> Image:
        """

        prints a plot of this distribution - other distribution with matplotlib
        :returns the pyplot figure for plot
                 <Image>
        """

    @abc.abstractmethod
    def get_compare(
        self,
        other_probability: "IProbabilityDistribution",
        this_distribution_name: str,
        other_distribution_name: str,
    ) -> Image:
        """

        prints a plot of this at least this distribution alongside another distribution with matplotlib
        :returns the pyplot figure for plot
                 <Image>
        """

    @abc.abstractmethod
    def get_compare_at_least(
        self,
        other_probability: "IProbabilityDistribution",
        this_distribution_name: str,
        other_distribution_name: str,
    ) -> Image:
        """

        prints a plot of this at least this distribution alongside another distribution with matplotlib
        :returns the pyplot figure for plot
                 <Image>
        """

    @abc.abstractmethod
    def get_compare_at_most(
        self,
        other_probability: "IProbabilityDistribution",
        this_distribution_name: str,
        other_distribution_name: str,
    ) -> Image:
        """

        prints a plot of this at most this distribution alongside another distribution with matplotlib
        :returns the pyplot figure for plot
                 <Image>
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
    def average(self) -> float:
        """

        :return: returns the waited average of the distribution
                 <float>
        """

    @abc.abstractmethod
    def at_least(self) -> typing.Dict[int, float]:
        pass

    @abc.abstractmethod
    def at_most(self) -> typing.Dict[int, float]:
        pass

    @abc.abstractmethod
    def __add__(self, other: object) -> "IProbabilityDistribution":
        pass

    @abc.abstractmethod
    def __sub__(self, other: object) -> "IProbabilityDistribution":
        pass

    @abc.abstractmethod
    def __mul__(self, other: object) -> "IProbabilityDistribution":
        pass

    @abc.abstractmethod
    def __floordiv__(self, other: object) -> "IProbabilityDistribution":
        pass

    @abc.abstractmethod
    def __equal__(self, other: object) -> "IProbabilityDistribution":
        pass

    @abc.abstractmethod
    def __not_equal__(self, other: object) -> "IProbabilityDistribution":
        pass

    @abc.abstractmethod
    def __lt__(self, other: object) -> "IProbabilityDistribution":
        pass

    @abc.abstractmethod
    def __le__(self, other: object) -> "IProbabilityDistribution":
        pass

    @abc.abstractmethod
    def __gt__(self, other: object) -> "IProbabilityDistribution":
        pass

    @abc.abstractmethod
    def __ge__(self, other: object) -> "IProbabilityDistribution":
        pass

    @abc.abstractmethod
    def __and__(self, other: object) -> "IProbabilityDistribution":
        pass

    @abc.abstractmethod
    def __or__(self, other: object) -> "IProbabilityDistribution":
        pass

    @abc.abstractmethod
    def not_operator(self) -> "IProbabilityDistribution":
        pass

    @abc.abstractmethod
    def max_operator(self, other: object) -> "IProbabilityDistribution":
        pass

    @abc.abstractmethod
    def min_operator(self, other: object) -> "IProbabilityDistribution":
        pass

    @abc.abstractmethod
    def __str__(self) -> str:
        pass

    @abc.abstractmethod
    def __repr__(self) -> str:
        pass

    @abc.abstractmethod
    def __abs__(self) -> "IProbabilityOutcome":
        pass
