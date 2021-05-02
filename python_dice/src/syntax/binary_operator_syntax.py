from python_dice.interface.syntax.i_dice_syntax import IDiceSyntax


class BinaryOperatorSyntax(IDiceSyntax):
    TOKEN_NAME = "BINARY_OPERATOR"
    TOKEN_REGEX = r"==|!=|<=|<|>=|>|\bAND\b|\bOR\b"

    @staticmethod
    def get_token_name() -> str:
        return BinaryOperatorSyntax.TOKEN_NAME

    @staticmethod
    def get_token_regex() -> str:
        return BinaryOperatorSyntax.TOKEN_REGEX
