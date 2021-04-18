from python_dice.interface.syntax.i_dice_syntax import IDiceSyntax


class NotSyntax(IDiceSyntax):
    TOKEN_NAME = "NOT"
    TOKEN_REGEX = r"!(?!=)"

    @staticmethod
    def get_token_name() -> str:
        return NotSyntax.TOKEN_NAME

    @staticmethod
    def get_token_regex() -> str:
        return NotSyntax.TOKEN_REGEX
