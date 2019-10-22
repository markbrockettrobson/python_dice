# python dice

[![codecov](https://codecov.io/gh/markbrockettrobson/python_dice/branch/master/graph/badge.svg)](https://codecov.io/gh/markbrockettrobson/pydice)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![MIT](https://black.readthedocs.io/en/stable/_static/license.svg)

a statistical dice library for python

## to install
~~~
python -m pip install python_dice
~~~

## source at 
https://github.com/markbrockettrobson/python_dice

##Usage

~~~
from python_dice import PythonDiceInterpreter

interpreter = PythonDiceInterpreter()
program = [
    "VAR six_sided_dice = 1d6",
    "VAR two_six_sided_dice = 2d6",
    "VAR odds_of_snake_eyes = ( two_six_sided_dice == 2 ) ",
]
roll = interpreter.roll(program).get_constant("six_sided_dice")
print(roll)

> 3
~~~

~~~
interpreter = python_dice_interpreter.PythonDiceInterpreter()
        program = [
            "VAR save_roll = 1d20 + 8",
            "VAR burning_arch_damage = 9d6 + 9",
            "VAR pass_save = ( save_roll >= 19 ) ",
            "VAR damage_half_on_save = burning_arch_damage // (pass_save + 1)",
        ]
        interpreter.get_probability_distribution(program).get_var("damage_half_on_save").show_histogram()

~~~
![image of 9d6 add 9 half round up if 1d20 add 8 greater than 19](https://raw.githubusercontent.com/markbrockettrobson/python_dice/master/images/level_nine_burning_arc.png)

# Syntax

Set a var
~~~
VAR lower_case_name = 1
VAR name = 4d20
~~~
add, subtract, multiply, integer division
~~~
VAR name = 1 + 2d3 - 3 * 4d2 // 5
~~~
parenthesis
~~~
VAR out = 3 * ( 1 + 1d4 )
~~~
binary operator
~~~
VAR a = 1d4 == 1
VAR b = 1d4 != 1
VAR c = 1d4 <= 2
VAR d = 1d4 < 3
VAR e = 1d4 >= 2
VAR f = 1d4 >= 2
VAR g = (1d4 >= 2) AND !(1d20 == 2)
VAR h = (1d4 >= 2) OR !(1d20 == 2)
~~~
abs
~~~
var abs = ABS( 1d6 - 1d6 )
~~~
