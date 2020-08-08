import abc

import rply

import python_dice.src.probability_distribution as probability_distribution


class IDiceExpression(abc.ABC, rply.token.Token):
    @staticmethod
    @abc.abstractmethod
    def add_production_function(parser_generator: rply.ParserGenerator) -> None:
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
    def get_probability_distribution(
        self,
    ) -> probability_distribution.ProbabilityDistribution:
        """

        :return: the probability of the statement
        """
