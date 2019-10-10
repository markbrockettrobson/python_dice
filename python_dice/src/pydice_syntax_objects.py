import python_dice.src.pydice_syntax.add as add
import python_dice.src.pydice_syntax.constant_integer as constant_integer

LEXER_SYNTAX = [constant_integer.ConstantInteger, add.Add]

PRECEDENCE = [("left", ["ADD"])]
