from python_dice.interface.syntax.i_dice_syntax import IDiceSyntax


class NameSyntax(IDiceSyntax):
    TOKEN_NAME = "NAME"
    TOKEN_REGEX = r"\b[a-z_]+\b"

    @staticmethod
    def get_token_name() -> str:
        return NameSyntax.TOKEN_NAME

    @staticmethod
    def get_token_regex() -> str:
        return NameSyntax.TOKEN_REGEX
