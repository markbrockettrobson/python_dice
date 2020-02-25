import python_dice.interface.python_dice_syntax.i_dice_syntax as i_dice_statement
import python_dice.src.python_dice_syntax.dice_syntax_helper as dice_syntax_helper


class DiceSyntax(i_dice_statement.IDiceSyntax):
    TOKEN_NAME = "DICE"
    TOKEN_REGEX = dice_syntax_helper.DICE_SYNTAX

    @staticmethod
    def get_token_name() -> str:
        return DiceSyntax.TOKEN_NAME

    @staticmethod
    def get_token_regex() -> str:
        return DiceSyntax.TOKEN_REGEX
