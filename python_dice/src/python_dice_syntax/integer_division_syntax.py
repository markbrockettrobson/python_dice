import python_dice.interface.python_dice_syntax.i_dice_syntax as i_dice_statement


class IntegerDivisionSyntax(i_dice_statement.IDiceSyntax):
    TOKEN_NAME = "INTEGER_DIVISION"
    TOKEN_REGEX = r"//"

    @staticmethod
    def get_token_name() -> str:
        return IntegerDivisionSyntax.TOKEN_NAME

    @staticmethod
    def get_token_regex() -> str:
        return IntegerDivisionSyntax.TOKEN_REGEX
