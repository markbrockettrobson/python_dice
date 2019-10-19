import python_dice.interface.python_dice_syntax.i_dice_syntax as i_dice_statement


class NameSyntax(i_dice_statement.IDiceSyntax):
    TOKEN_NAME = "NAME"
    TOKEN_REGEX = r"\b[a-z_]+\b"

    @staticmethod
    def get_token_name() -> str:
        return NameSyntax.TOKEN_NAME

    @staticmethod
    def get_token_regex() -> str:
        return NameSyntax.TOKEN_REGEX
