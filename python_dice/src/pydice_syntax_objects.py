import python_dice.src.pydice_syntax.add as add
import python_dice.src.pydice_syntax.constant_integer as constant_integer
import python_dice.src.pydice_syntax.multiply as multiply
import python_dice.src.pydice_syntax.subtract as subtract

LEXER_SYNTAX = [
    constant_integer.ConstantInteger,
    add.Add,
    subtract.Subtract,
    multiply.Multiply,
]

PRECEDENCE = [
    ("left", [add.Add.get_token_name(), subtract.Subtract.get_token_name()]),
    ("left", [multiply.Multiply.get_token_name()]),
]
