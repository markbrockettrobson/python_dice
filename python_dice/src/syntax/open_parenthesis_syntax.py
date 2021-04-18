from python_dice.interface.syntax.i_dice_syntax import IDiceSyntax


class OpenParenthesisSyntax(IDiceSyntax):
    TOKEN_NAME = "OPEN_PARENTHESIS"
    TOKEN_REGEX = r"\("

    @staticmethod
    def get_token_name() -> str:
        return OpenParenthesisSyntax.TOKEN_NAME

    @staticmethod
    def get_token_regex() -> str:
        return OpenParenthesisSyntax.TOKEN_REGEX
