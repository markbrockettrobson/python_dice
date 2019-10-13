import python_dice.src.python_dice_parser as python_dice_parser

parser = python_dice_parser.PythonDiceParser()
code = "(40d6 // 10d4)"

program = parser.parse(code)
print(program.roll())
print(program.max())
print(program.min())
program.get_probability_distribution().show_histogram()
