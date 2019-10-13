import python_dice.interface.python_dice_syntax.i_dice_syntax as i_dice_statement


class ConstantBinarySyntax(i_dice_statement.IDiceSyntax):
    TOKEN_NAME = "CONSTANT_BINARY"
    TOKEN_REGEX = r"\bTrue\b|\bFalse\b"

    @staticmethod
    def get_token_name() -> str:
        return ConstantBinarySyntax.TOKEN_NAME

    @staticmethod
    def get_token_regex() -> str:
        return ConstantBinarySyntax.TOKEN_REGEX
