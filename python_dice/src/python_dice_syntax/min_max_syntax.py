import python_dice.interface.python_dice_syntax.i_dice_syntax as i_dice_statement


class MinMaxSyntax(i_dice_statement.IDiceSyntax):
    TOKEN_NAME = "MINMAX"
    TOKEN_REGEX = r"\bMAX\b|\bMIN\b"

    @staticmethod
    def get_token_name() -> str:
        return MinMaxSyntax.TOKEN_NAME

    @staticmethod
    def get_token_regex() -> str:
        return MinMaxSyntax.TOKEN_REGEX
