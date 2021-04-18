from python_dice.interface.syntax.i_dice_syntax import IDiceSyntax


class SubtractSyntax(IDiceSyntax):
    TOKEN_NAME = "SUBTRACT"
    TOKEN_REGEX = r"\-"

    @staticmethod
    def get_token_name() -> str:
        return SubtractSyntax.TOKEN_NAME

    @staticmethod
    def get_token_regex() -> str:
        return SubtractSyntax.TOKEN_REGEX
