import python_dice.src.python_dice_syntax.add as add
import python_dice.src.python_dice_syntax.constant_integer as constant_integer
import python_dice.src.python_dice_syntax.integer_division as integer_division
import python_dice.src.python_dice_syntax.multiply as multiply
import python_dice.src.python_dice_syntax.subtract as subtract

LEXER_SYNTAX = [
    constant_integer.ConstantInteger,
    add.Add,
    subtract.Subtract,
    multiply.Multiply,
    integer_division.IntegerDivision,
]

PRECEDENCE = [
    ("left", [add.Add.get_token_name(), subtract.Subtract.get_token_name()]),
    (
        "left",
        [
            integer_division.IntegerDivision.get_token_name(),
            multiply.Multiply.get_token_name(),
        ],
    ),
]
