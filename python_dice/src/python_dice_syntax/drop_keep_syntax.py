import python_dice.interface.python_dice_syntax.i_dice_syntax as i_dice_statement
import python_dice.src.python_dice_syntax.dice_syntax_helper as dice_syntax_helper


class DropKeepSyntax(i_dice_statement.IDiceSyntax):
    TOKEN_NAME = "DROP_KEEP_DICE"
    TOKEN_REGEX = dice_syntax_helper.DROP_KEEP_DICE_SYNTAX

    @staticmethod
    def get_token_name() -> str:
        return DropKeepSyntax.TOKEN_NAME

    @staticmethod
    def get_token_regex() -> str:
        return DropKeepSyntax.TOKEN_REGEX
