from python_dice.interface.syntax.i_dice_syntax import IDiceSyntax


class MinMaxSyntax(IDiceSyntax):
    TOKEN_NAME = "MINMAX"
    TOKEN_REGEX = r"\bMAX\b|\bMIN\b"

    @staticmethod
    def get_token_name() -> str:
        return MinMaxSyntax.TOKEN_NAME

    @staticmethod
    def get_token_regex() -> str:
        return MinMaxSyntax.TOKEN_REGEX
