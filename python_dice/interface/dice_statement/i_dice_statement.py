import abc


class IDiceSyntax(abc.ABC):
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
