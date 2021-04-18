from python_dice.interface.syntax.i_dice_syntax import IDiceSyntax


class AddSyntax(IDiceSyntax):
    TOKEN_NAME = "ADD"
    TOKEN_REGEX = r"\+"

    @staticmethod
    def get_token_name() -> str:
        return AddSyntax.TOKEN_NAME

    @staticmethod
    def get_token_regex() -> str:
        return AddSyntax.TOKEN_REGEX
