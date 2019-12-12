# python dice ![logo](https://raw.githubusercontent.com/markbrockettrobson/python_dice/master/images/pythondice_logo_128x128.png)


[![codecov](https://codecov.io/gh/markbrockettrobson/python_dice/branch/master/graph/badge.svg)](https://codecov.io/gh/markbrockettrobson/pydice)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![MIT](https://black.readthedocs.io/en/stable/_static/license.svg)

a statistical dice library for python


### to install
~~~
python -m pip install python_dice
~~~

### source at 
https://github.com/markbrockettrobson/python_dice

### Usage

~~~
from python_dice import PythonDiceInterpreter

interpreter = PythonDiceInterpreter()
program = ["1d6"]
roll = interpreter.roll(program)["stdout"]
print(roll)

> 3
~~~

~~~
from python_dice import PythonDiceInterpreter

interpreter = PythonDiceInterpreter()
program = [
     "VAR one_dice = 1d6 + 10",
     "VAR two_dice = 1d6 - 10"
]
roll_one = interpreter.max(program)["one_dice"]
roll_two = interpreter.min(program)["two_dice"]
print(roll_one, roll_two)

> 16 -9
~~~

~~~
interpreter = python_dice_interpreter.PythonDiceInterpreter()
program = [
    "VAR save_roll = 1d20",
    "VAR burning_arch_damage = 10d6 + 10",
    "VAR pass_save = ( save_roll >= 10 ) ",
    "VAR damage_half_on_save = burning_arch_damage // (pass_save + 1)",
    "damage_half_on_save"
]
im = interpreter.get_histogram(program)
im.show()
~~~
![image of 10d6 add 10 half round up if 1d20 greater than 10](https://raw.githubusercontent.com/markbrockettrobson/python_dice/master/images/histogram.png)

### Syntax

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
VAR f = 1d4 > 2
VAR g = (1d4 >= 2) AND !(1d20 == 2)
VAR h = (1d4 >= 2) OR !(1d20 == 2)
~~~
abs
~~~
var abs = ABS( 1d6 - 1d6 )
~~~
