from python_dice.interface.syntax.i_dice_syntax import IDiceSyntax
from python_dice.src.syntax.dice_syntax_helper import DICE_SYNTAX


class DiceSyntax(IDiceSyntax):
    TOKEN_NAME = "DICE"
    TOKEN_REGEX = DICE_SYNTAX

    @staticmethod
    def get_token_name() -> str:
        return DiceSyntax.TOKEN_NAME

    @staticmethod
    def get_token_regex() -> str:
        return DiceSyntax.TOKEN_REGEX
