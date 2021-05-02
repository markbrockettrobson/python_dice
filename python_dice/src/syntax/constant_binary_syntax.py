from python_dice.interface.syntax.i_dice_syntax import IDiceSyntax


class ConstantBinarySyntax(IDiceSyntax):
    TOKEN_NAME = "CONSTANT_BINARY"
    TOKEN_REGEX = r"\bTrue\b|\bFalse\b"

    @staticmethod
    def get_token_name() -> str:
        return ConstantBinarySyntax.TOKEN_NAME

    @staticmethod
    def get_token_regex() -> str:
        return ConstantBinarySyntax.TOKEN_REGEX
