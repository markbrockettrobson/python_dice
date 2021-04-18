from python_dice.interface.syntax.i_dice_syntax import IDiceSyntax


class AssignmentSyntax(IDiceSyntax):
    TOKEN_NAME = "ASSIGNMENT"
    TOKEN_REGEX = r"=(?!=)(?<!==)"

    @staticmethod
    def get_token_name() -> str:
        return AssignmentSyntax.TOKEN_NAME

    @staticmethod
    def get_token_regex() -> str:
        return AssignmentSyntax.TOKEN_REGEX
