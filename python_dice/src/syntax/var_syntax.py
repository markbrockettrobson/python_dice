from python_dice.interface.syntax.i_dice_syntax import IDiceSyntax


class VarSyntax(IDiceSyntax):
    TOKEN_NAME = "VAR"
    TOKEN_REGEX = r"\bVAR\b"

    @staticmethod
    def get_token_name() -> str:
        return VarSyntax.TOKEN_NAME

    @staticmethod
    def get_token_regex() -> str:
        return VarSyntax.TOKEN_REGEX
