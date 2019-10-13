import python_dice.interface.python_dice_syntax.i_dice_syntax as i_dice_statement


class OpenParenthesisSyntax(i_dice_statement.IDiceSyntax):
    TOKEN_NAME = "OPEN_PARENTHESIS"
    TOKEN_REGEX = r"\("

    @staticmethod
    def get_token_name() -> str:
        return OpenParenthesisSyntax.TOKEN_NAME

    @staticmethod
    def get_token_regex() -> str:
        return OpenParenthesisSyntax.TOKEN_REGEX
