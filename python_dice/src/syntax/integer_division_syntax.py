from python_dice.interface.syntax.i_dice_syntax import IDiceSyntax


class IntegerDivisionSyntax(IDiceSyntax):
    TOKEN_NAME = "INTEGER_DIVISION"
    TOKEN_REGEX = r"//"

    @staticmethod
    def get_token_name() -> str:
        return IntegerDivisionSyntax.TOKEN_NAME

    @staticmethod
    def get_token_regex() -> str:
        return IntegerDivisionSyntax.TOKEN_REGEX
