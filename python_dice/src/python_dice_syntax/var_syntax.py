import python_dice.interface.python_dice_syntax.i_dice_syntax as i_dice_statement


class VarSyntax(i_dice_statement.IDiceSyntax):
    TOKEN_NAME = "VAR"
    TOKEN_REGEX = r"\bVAR\b"

    @staticmethod
    def get_token_name() -> str:
        return VarSyntax.TOKEN_NAME

    @staticmethod
    def get_token_regex() -> str:
        return VarSyntax.TOKEN_REGEX
