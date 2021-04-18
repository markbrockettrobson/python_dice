import abc
import typing

import rply  # type: ignore

from python_dice.interface.probability_distribution.i_probability_distribution import IProbabilityDistribution


class IDiceExpression(abc.ABC, rply.token.Token):
    @staticmethod
    @abc.abstractmethod
    def add_production_function(parser_generator: rply.ParserGenerator) -> typing.Callable:
        """

        add a production rule to the parser generator
        """

    @abc.abstractmethod
    def roll(self) -> int:
        """

        :return: returns the result of a roll of the dice
                 <int>
        """

    @abc.abstractmethod
    def max(self) -> int:
        """

        :return: returns a largest possible result of a roll of the dice
                 <int>
        """

    @abc.abstractmethod
    def min(self) -> int:
        """

        :return: returns a smallest possible result of a roll of the dice
                 <int>
        """

    @abc.abstractmethod
    def estimated_cost(self) -> int:
        """

        :return: returns a estimated cost of the python dice expression
                 <int>
        """

    @abc.abstractmethod
    def get_probability_distribution(self) -> IProbabilityDistribution:
        """

        :return: the probability of the statement
        """

    @abc.abstractmethod
    def get_contained_variables(
        self,
    ) -> typing.Set[str]:
        """

        :return: the set of contained variables of the statement
        """
