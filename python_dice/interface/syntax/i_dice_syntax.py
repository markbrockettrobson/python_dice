import abc

import rply  # type: ignore


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
