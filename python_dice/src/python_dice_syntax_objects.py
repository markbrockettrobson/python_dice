from typing import List, Type

from python_dice.interface.expression.i_dice_expression import IDiceExpression
from python_dice.interface.syntax.i_dice_syntax import IDiceSyntax
from python_dice.src.expression.abs_expression import AbsExpression
from python_dice.src.expression.add_expression import AddExpression
from python_dice.src.expression.binary_operator_expression import BinaryOperatorExpression
from python_dice.src.expression.constant_binary_expression import ConstantBinaryExpression
from python_dice.src.expression.constant_integer_expression import ConstantIntegerExpression
from python_dice.src.expression.dice_expression import DiceExpression
from python_dice.src.expression.drop_keep_expression import DropKeepExpression
from python_dice.src.expression.get_var_expression import GetVarExpression
from python_dice.src.expression.integer_division_expression import IntegerDivisionExpression
from python_dice.src.expression.minmax_expression import MinMaxExpression
from python_dice.src.expression.multiply_expression import MultiplyExpression
from python_dice.src.expression.not_expression import NotExpression
from python_dice.src.expression.parentheses_enclosed_expression import ParenthesisEnclosedExpression
from python_dice.src.expression.subtract_expression import SubtractExpression
from python_dice.src.expression.var_assignment_expression import VarAssignmentExpression
from python_dice.src.syntax.abs_syntax import AbsSyntax
from python_dice.src.syntax.add_syntax import AddSyntax
from python_dice.src.syntax.assignment_syntax import AssignmentSyntax
from python_dice.src.syntax.binary_operator_syntax import BinaryOperatorSyntax
from python_dice.src.syntax.close_parenthesis_syntax import CloseParenthesisSyntax
from python_dice.src.syntax.comma_syntax import CommaSyntax
from python_dice.src.syntax.constant_binary_syntax import ConstantBinarySyntax
from python_dice.src.syntax.constant_integer_syntax import ConstantIntegerSyntax
from python_dice.src.syntax.dice_syntax import DiceSyntax
from python_dice.src.syntax.drop_keep_syntax import DropKeepSyntax
from python_dice.src.syntax.integer_division_syntax import IntegerDivisionSyntax
from python_dice.src.syntax.min_max_syntax import MinMaxSyntax
from python_dice.src.syntax.multiply_syntax import MultiplySyntax
from python_dice.src.syntax.name_syntax import NameSyntax
from python_dice.src.syntax.not_syntax import NotSyntax
from python_dice.src.syntax.open_parenthesis_syntax import OpenParenthesisSyntax
from python_dice.src.syntax.subtract_syntax import SubtractSyntax
from python_dice.src.syntax.var_syntax import VarSyntax

LEXER_SYNTAX: List[Type[IDiceSyntax]] = [
    OpenParenthesisSyntax,
    CloseParenthesisSyntax,
    CommaSyntax,
    NotSyntax,
    DropKeepSyntax,
    DiceSyntax,
    BinaryOperatorSyntax,
    ConstantIntegerSyntax,
    ConstantBinarySyntax,
    AddSyntax,
    SubtractSyntax,
    MultiplySyntax,
    IntegerDivisionSyntax,
    MinMaxSyntax,
    AbsSyntax,
    AssignmentSyntax,
    VarSyntax,
    NameSyntax,
]

PARSER_EXPRESSIONS: List[Type[IDiceExpression]] = [
    ParenthesisEnclosedExpression,
    NotExpression,
    DropKeepExpression,
    DiceExpression,
    ConstantIntegerExpression,
    ConstantBinaryExpression,
    AddExpression,
    SubtractExpression,
    MultiplyExpression,
    IntegerDivisionExpression,
    BinaryOperatorExpression,
    MinMaxExpression,
    AbsExpression,
    VarAssignmentExpression,
    GetVarExpression,
]

PRECEDENCE = [
    ("nonassoc", [VarSyntax.get_token_name()]),
    ("left", [AssignmentSyntax.get_token_name()]),
    ("left", [OpenParenthesisSyntax.get_token_name()]),
    ("left", [NotSyntax.get_token_name()]),
    (
        "left",
        [
            AddSyntax.get_token_name(),
            SubtractSyntax.get_token_name(),
        ],
    ),
    (
        "left",
        [
            IntegerDivisionSyntax.get_token_name(),
            MultiplySyntax.get_token_name(),
        ],
    ),
    ("left", [BinaryOperatorSyntax.get_token_name()]),
]
