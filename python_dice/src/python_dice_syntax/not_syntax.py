import python_dice.interface.python_dice_syntax.i_dice_syntax as i_dice_statement


class NotSyntax(i_dice_statement.IDiceSyntax):
    TOKEN_NAME = "NOT"
    TOKEN_REGEX = r"!(?!=)"

    @staticmethod
    def get_token_name() -> str:
        return NotSyntax.TOKEN_NAME

    @staticmethod
    def get_token_regex() -> str:
        return NotSyntax.TOKEN_REGEX
