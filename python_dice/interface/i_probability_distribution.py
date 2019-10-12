import abc
import typing


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
    def show_histogram(self) -> None:
        """

        prints a plot of the distribution with matplotlib
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
