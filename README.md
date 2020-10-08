# Python dice ![logo](https://raw.githubusercontent.com/markbrockettrobson/python_dice/master/images/pythondice_logo_128x128.png)


[![codecov](https://codecov.io/gh/markbrockettrobson/python_dice/branch/master/graph/badge.svg)](https://codecov.io/gh/markbrockettrobson/pydice)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![license](https://i.creativecommons.org/l/by-nc-sa/4.0/80x15.png)

a statistical dice engine for python

### License 

This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License
http://creativecommons.org/licenses/by-nc-sa/4.0/

### To install
~~~
python -m pip install python_dice
~~~

### Source at 
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
     "VAR a_name = d6 + 10",
     "VAR b_name = d6 - 10"
]
a_name = interpreter.max(program)["a_name"]
b_name = interpreter.min(program)["b_name"]
print(a_name, b_name)

> 16 -9
~~~

~~~
interpreter = python_dice_interpreter.PythonDiceInterpreter()
program = [
    "VAR save_roll = d20",
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
#### Dice
~~~
<number of dice to roll>d<number of sides on the dice>
4d10
d6
1d%
30dF
2d[1,1,2,3,5,8]
~~~

number of dice is missing will be treated as one. <br>
number of sides can also be:<br>
+ % for 100.
+ F for fate dice [-1,0,1].
+ custom dice with a comma separated list of side values in [ ] square brackets (trailing comma allowed).
+ range of values d[1,2,3,4,5] == d[1-5] ==d5
  + d[-5,-4,-3,-2] == d[-5--2] == d[-2--5]
+ multiplier for many equal sides d[1,1,1,1,1,1,1,8] == d[1*7, 8]
  + d[1,1,1,2,2,3,3,4] == d[1-3*2,1,4] 


#### Keep Drop
~~~
<number of dice to roll>d<number of sides on the dice>[k for keep d for drop]<number of dice to keep or drop>
2d20k1  roll 2 d20's take the highest 1
16d%k10 roll 16 d% keep the hightest 10
10d[-1,1]d5  roll 10 d[-1,1]'s drop the highest 5
2dFd1  roll 2 dF's drop the highest 1
~~~

If the number of dice to keep is set above the number of dice to roll it will keep all dice. <br>
If the number to drop is equal or greater then the number of dice to roll it will always roll 0. <br>
If the number of dice to keep is set to zero then it will always roll 0. <br>
If the number of dice to drop is set to zero then it will be ignored. <br>

#### Set a var
~~~
VAR lower_case_name = 1
VAR name = 4d20
~~~
#### Add, subtract, multiply, integer division
~~~
VAR name = 1 + 2d3 - 3 * 4d2 // 5
~~~
#### Parenthesis
~~~
VAR out = 3 * ( 1 + 1d4 )
~~~
#### Binary operator
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
for non binary values, values above 0 are considered true.

#### Abs
~~~
VAR abs = ABS( 1d6 - 1d6 )
~~~
#### Min and Max
~~~
MAX(4d7, 2d10)
MIN(50, d%)
~~~