import abc

import rply

import python_dice.src.probability_distribution as probability_distribution


class IDiceSyntax(abc.ABC, rply.token.BaseBox):
    @staticmethod
    @abc.abstractmethod
    def get_token_name() -> str:
        """

        :return: the token name for this syntax
                 <str>
        """

    @staticmethod
    @abc.abstractmethod
    def get_token_regex() -> str:
        """

        :return: the token regex for this syntax
                 <str>
        """
