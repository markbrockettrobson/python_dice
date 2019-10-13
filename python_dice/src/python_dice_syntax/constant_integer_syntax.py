import python_dice.interface.python_dice_syntax.i_dice_syntax as i_dice_statement


class ConstantIntegerSyntax(i_dice_statement.IDiceSyntax):
    TOKEN_NAME = "CONSTANT_INTEGER"
    TOKEN_REGEX = r"-?\d+"

    @staticmethod
    def get_token_name() -> str:
        return ConstantIntegerSyntax.TOKEN_NAME

    @staticmethod
    def get_token_regex() -> str:
        return ConstantIntegerSyntax.TOKEN_REGEX

    def __init__(self, number: str):
        self._number = number
