import python_dice.src.python_dice_expression.add_expression as add_expression
import python_dice.src.python_dice_expression.constant_integer_expression as constant_integer_expression
import python_dice.src.python_dice_expression.dice_expression as dice_expression
import python_dice.src.python_dice_expression.integer_division_expression as integer_division_expression
import python_dice.src.python_dice_expression.multiply_expression as multiply_expression
import python_dice.src.python_dice_expression.subtract_expression as subtract_expression
import python_dice.src.python_dice_syntax.add_syntax as add_syntax
import python_dice.src.python_dice_syntax.constant_integer_syntax as constant_integer_syntax
import python_dice.src.python_dice_syntax.dice_syntax as dice_syntax
import python_dice.src.python_dice_syntax.integer_division_syntax as integer_division_syntax
import python_dice.src.python_dice_syntax.multiply_syntax as multiply_syntax
import python_dice.src.python_dice_syntax.subtract_syntax as subtract_syntax

LEXER_SYNTAX = [
    dice_syntax.DiceSyntax,
    constant_integer_syntax.ConstantIntegerSyntax,
    add_syntax.AddSyntax,
    subtract_syntax.SubtractSyntax,
    multiply_syntax.MultiplySyntax,
    integer_division_syntax.IntegerDivisionSyntax,
]

LEXER_Expression = [
    dice_expression.DiceExpression,
    constant_integer_expression.ConstantIntegerExpression,
    add_expression.AddExpression,
    subtract_expression.SubtractExpression,
    multiply_expression.MultiplyExpression,
    integer_division_expression.IntegerDivisionExpression,
]

PRECEDENCE = [
    (
        "left",
        [
            add_syntax.AddSyntax.get_token_name(),
            subtract_syntax.SubtractSyntax.get_token_name(),
        ],
    ),
    (
        "left",
        [
            integer_division_syntax.IntegerDivisionSyntax.get_token_name(),
            multiply_syntax.MultiplySyntax.get_token_name(),
        ],
    ),
]
