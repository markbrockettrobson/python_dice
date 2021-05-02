from python_dice.interface.syntax.i_dice_syntax import IDiceSyntax


class MultiplySyntax(IDiceSyntax):
    TOKEN_NAME = "MULTIPLY"
    TOKEN_REGEX = r"\*"

    @staticmethod
    def get_token_name() -> str:
        return MultiplySyntax.TOKEN_NAME

    @staticmethod
    def get_token_regex() -> str:
        return MultiplySyntax.TOKEN_REGEX
