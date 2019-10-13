import python_dice.interface.python_dice_syntax.i_dice_syntax as i_dice_statement


class AddSyntax(i_dice_statement.IDiceSyntax):
    TOKEN_NAME = "ADD"
    TOKEN_REGEX = r"\+"

    @staticmethod
    def get_token_name() -> str:
        return AddSyntax.TOKEN_NAME

    @staticmethod
    def get_token_regex() -> str:
        return AddSyntax.TOKEN_REGEX
