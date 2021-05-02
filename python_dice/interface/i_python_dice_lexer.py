from abc import ABC, abstractmethod


class IPythonDiceLexer(ABC):
    @abstractmethod
    def lex(self, input_text: str):
        """

        :return: a list of lexer tokens built from the input text
        """
