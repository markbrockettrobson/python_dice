import python_dice.interface.python_dice_syntax.i_dice_syntax as i_dice_statement


class DiceSyntax(i_dice_statement.IDiceSyntax):
    TOKEN_NAME = "DICE"
    TOKEN_REGEX = r"\d*d(\d+|%)"

    @staticmethod
    def get_token_name() -> str:
        return DiceSyntax.TOKEN_NAME

    @staticmethod
    def get_token_regex() -> str:
        return DiceSyntax.TOKEN_REGEX
