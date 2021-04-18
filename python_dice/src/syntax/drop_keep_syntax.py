from python_dice.interface.syntax.i_dice_syntax import IDiceSyntax
from python_dice.src.syntax.dice_syntax_helper import DROP_KEEP_DICE_SYNTAX


class DropKeepSyntax(IDiceSyntax):
    TOKEN_NAME = "DROP_KEEP_DICE"
    TOKEN_REGEX = DROP_KEEP_DICE_SYNTAX

    @staticmethod
    def get_token_name() -> str:
        return DropKeepSyntax.TOKEN_NAME

    @staticmethod
    def get_token_regex() -> str:
        return DropKeepSyntax.TOKEN_REGEX
