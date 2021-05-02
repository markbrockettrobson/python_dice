from abc import ABC, abstractmethod
from typing import Callable, Set

import rply  # type: ignore

from python_dice.interface.probability_distribution.i_probability_distribution import IProbabilityDistribution
from python_dice.interface.probability_distribution.i_probability_distribution_factory import (
    IProbabilityDistributionFactory,
)


class IDiceExpression(ABC, rply.token.Token):
    @staticmethod
    @abstractmethod
    def add_production_function(
        parser_generator: rply.ParserGenerator, probability_distribution_factory: IProbabilityDistributionFactory
    ) -> Callable:
        """

        add a production rule to the parser generator
        """

    @abstractmethod
    def roll(self) -> int:
        """

        :return: returns the result of a roll of the dice
                 <int>
        """

    @abstractmethod
    def max(self) -> int:
        """

        :return: returns a largest possible result of a roll of the dice
                 <int>
        """

    @abstractmethod
    def min(self) -> int:
        """

        :return: returns a smallest possible result of a roll of the dice
                 <int>
        """

    @abstractmethod
    def estimated_cost(self) -> int:
        """

        :return: returns a estimated cost of the python dice expression
                 <int>
        """

    @abstractmethod
    def get_probability_distribution(self) -> IProbabilityDistribution:
        """

        :return: the probability of the statement
        """

    @abstractmethod
    def get_contained_variables(
        self,
    ) -> Set[str]:
        """

        :return: the set of contained variables of the statement
        """
