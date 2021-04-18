from python_dice.interface.syntax.i_dice_syntax import IDiceSyntax


class CommaSyntax(IDiceSyntax):
    TOKEN_NAME = "COMMA"
    TOKEN_REGEX = r"\,"

    @staticmethod
    def get_token_name() -> str:
        return CommaSyntax.TOKEN_NAME

    @staticmethod
    def get_token_regex() -> str:
        return CommaSyntax.TOKEN_REGEX
