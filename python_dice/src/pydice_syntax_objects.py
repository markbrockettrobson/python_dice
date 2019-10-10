import python_dice.src.pydice_syntax.add as add
import python_dice.src.pydice_syntax.constant_integer as constant_integer
import python_dice.src.pydice_syntax.subtract as subtract

LEXER_SYNTAX = [constant_integer.ConstantInteger, add.Add, subtract.Subtract]

PRECEDENCE = [("left", ["ADD", "SUBTRACT"])]
