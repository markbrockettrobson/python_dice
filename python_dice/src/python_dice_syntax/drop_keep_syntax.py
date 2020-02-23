import python_dice.interface.python_dice_syntax.i_dice_syntax as i_dice_statement


class DropKeepSyntax(i_dice_statement.IDiceSyntax):
    TOKEN_NAME = "DROP_KEEP_DICE"
    TOKEN_REGEX = r"\d*d(\d+|%|F|\[(\s*(-?)\d+\s*,\s*)*(-?)\d+\s*(,?)\s*])[kd]\d+"

    @staticmethod
    def get_token_name() -> str:
        return DropKeepSyntax.TOKEN_NAME

    @staticmethod
    def get_token_regex() -> str:
        return DropKeepSyntax.TOKEN_REGEX
