from python_dice.interface.syntax.i_dice_syntax import IDiceSyntax


class ConstantIntegerSyntax(IDiceSyntax):
    TOKEN_NAME = "CONSTANT_INTEGER"
    TOKEN_REGEX = r"-?\d+"

    @staticmethod
    def get_token_name() -> str:
        return ConstantIntegerSyntax.TOKEN_NAME

    @staticmethod
    def get_token_regex() -> str:
        return ConstantIntegerSyntax.TOKEN_REGEX
