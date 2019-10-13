import python_dice.interface.python_dice_syntax.i_dice_syntax as i_dice_statement


class BinaryOperatorSyntax(i_dice_statement.IDiceSyntax):
    TOKEN_NAME = "BINARY_OPERATOR"
    TOKEN_REGEX = r"==|!=|<=|<|>=|>|\bAND\b|\bOR\b"

    @staticmethod
    def get_token_name() -> str:
        return BinaryOperatorSyntax.TOKEN_NAME

    @staticmethod
    def get_token_regex() -> str:
        return BinaryOperatorSyntax.TOKEN_REGEX
