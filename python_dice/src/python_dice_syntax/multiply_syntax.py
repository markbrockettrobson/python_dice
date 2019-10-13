import python_dice.interface.python_dice_syntax.i_dice_syntax as i_dice_statement


class MultiplySyntax(i_dice_statement.IDiceSyntax):
    TOKEN_NAME = "MULTIPLY"
    TOKEN_REGEX = r"\*"

    @staticmethod
    def get_token_name() -> str:
        return MultiplySyntax.TOKEN_NAME

    @staticmethod
    def get_token_regex() -> str:
        return MultiplySyntax.TOKEN_REGEX
