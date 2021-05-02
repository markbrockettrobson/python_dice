from python_dice.interface.syntax.i_dice_syntax import IDiceSyntax


class CloseParenthesisSyntax(IDiceSyntax):
    TOKEN_NAME = "CLOSE_PARENTHESIS"
    TOKEN_REGEX = r"\)"

    @staticmethod
    def get_token_name() -> str:
        return CloseParenthesisSyntax.TOKEN_NAME

    @staticmethod
    def get_token_regex() -> str:
        return CloseParenthesisSyntax.TOKEN_REGEX
