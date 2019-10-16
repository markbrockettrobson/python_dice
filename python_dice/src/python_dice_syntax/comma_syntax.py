import python_dice.interface.python_dice_syntax.i_dice_syntax as i_dice_statement


class CommaSyntax(i_dice_statement.IDiceSyntax):
    TOKEN_NAME = "COMMA"
    TOKEN_REGEX = r"\,"

    @staticmethod
    def get_token_name() -> str:
        return CommaSyntax.TOKEN_NAME

    @staticmethod
    def get_token_regex() -> str:
        return CommaSyntax.TOKEN_REGEX
