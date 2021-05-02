from abc import ABC, abstractmethod

import rply  # type: ignore


class IDiceSyntax(ABC, rply.token.BaseBox):
    @staticmethod
    @abstractmethod
    def get_token_name() -> str:
        """

        :return: the token name for this syntax
                 <str>
        """

    @staticmethod
    @abstractmethod
    def get_token_regex() -> str:
        """

        :return: the token regex for this syntax
                 <str>
        """
