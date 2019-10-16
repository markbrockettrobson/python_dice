import python_dice.interface.python_dice_syntax.i_dice_syntax as i_dice_statement


class AbsSyntax(i_dice_statement.IDiceSyntax):
    TOKEN_NAME = "ABS"
    TOKEN_REGEX = r"\bABS\b"

    @staticmethod
    def get_token_name() -> str:
        return AbsSyntax.TOKEN_NAME

    @staticmethod
    def get_token_regex() -> str:
        return AbsSyntax.TOKEN_REGEX
