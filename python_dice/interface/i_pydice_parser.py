import abc


class IPyDiceParser(abc.ABC):
    @abc.abstractmethod
    def parse(self, input_text: str):
        """

        :return: output of pydice program
        """
