from python_dice.interface.syntax.i_dice_syntax import IDiceSyntax


class AbsSyntax(IDiceSyntax):
    TOKEN_NAME = "ABS"
    TOKEN_REGEX = r"\bABS\b"

    @staticmethod
    def get_token_name() -> str:
        return AbsSyntax.TOKEN_NAME

    @staticmethod
    def get_token_regex() -> str:
        return AbsSyntax.TOKEN_REGEX
