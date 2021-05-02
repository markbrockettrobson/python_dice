import timeit
import typing
import unittest

from python_dice.src.python_dice_interpreter import PythonDiceInterpreter


class TestCost(unittest.TestCase):
    @staticmethod
    def do_not_run_test_estimated_cost_in_order():
        programs: typing.List[typing.List[str]] = [
            ["25d25"],
            ["25d30"],
            ["30d30"],
            ["30d25"],
            ["25d20"],
            ["20d25"],
            ["25d25 + 30"],
            ["25d30 + 30"],
            ["30d25 + 30"],
            ["30d30 + 30"],
            ["25d25 - 30"],
            ["25d30 - 30"],
            ["30d25 - 30"],
            ["30d30 - 30"],
            ["25d25 * 30"],
            ["25d30 * 30"],
            ["30d25 * 30"],
            ["30d30 * 30"],
            ["25d25 // 30"],
            ["25d30 // 30"],
            ["30d25 // 30"],
            ["30d30 // 30"],
            ["30d30 + 10d10"],
            ["30d35 + 10d10"],
            ["35d35 + 10d10"],
            ["35d30 + 10d10"],
            ["30d30 - 10d10"],
            ["30d35 - 10d10"],
            ["35d35 - 10d10"],
            ["35d30 - 10d10"],
            ["30d30 * 10d10"],
            ["30d35 * 10d10"],
            ["35d35 * 10d10"],
            ["35d30 * 10d10"],
            ["30d30 // 10d10"],
            ["30d35 // 10d10"],
            ["35d35 // 10d10"],
            ["35d30 // 10d10"],
            ["(30d30)"],
            ["(25d35)"],
            ["(30d30 + 30)"],
            ["(35d40 - 30)"],
            ["(35d35 * 30)"],
            ["(35d30 // 30)"],
            ["(35d35 - 10d10)"],
            ["(35d35 * 10d10)"],
            ["10d[0--10*2,1-10]"],
            ["ABS( 10d[0--10*2,1-10] )"],
            ["MAX( 10d[0--10*2,1-10] , 2d%)"],
            ["MIN( 10d[0--10*2,1-10] , 2d%)"],
            ["10d[2,4,6,8,10] == 20d10"],
            ["10d[2,4,6,8,10] <= 20d10"],
            ["10d[2,4,6,8,10] < 20d10"],
            ["10d[2,4,6,8,10] > 20d10"],
            ["10d[2,4,6,8,10] >= 20d10"],
            ["10d[2,4,6,8,10] != 20d10"],
            ["10d[-10,-8,-4,-2,0,2,4,6,8,10] AND 20d[-5-5]"],
            ["10d[-10,-8,-4,-2,0,2,4,6,8,10] OR 20d[-5-5]"],
            ["!(10d[2,4,6,8,10] == 20d10)"],
            ["!(10d[2,4,6,8,10] <= 20d10)"],
            ["!(10d[2,4,6,8,10] < 20d10)"],
            ["!(10d[2,4,6,8,10] > 20d10)"],
            ["!(10d[2,4,6,8,10] >= 20d10)"],
            ["!(10d[2,4,6,8,10] != 20d10)"],
            ["!(10d[-10,-8,-4,-2,0,2,4,6,8,10] AND 20d[-5-5])"],
            ["!(10d[-10,-8,-4,-2,0,2,4,6,8,10] OR 20d[-5-5])"],
            [
                "VAR save_roll = d20",
                "VAR burning_arch_damage = 10d6 + 10",
                "VAR pass_save = ( save_roll >= 10 ) ",
                "VAR damage_half_on_save = burning_arch_damage // (pass_save + 1)",
                "damage_half_on_save",
            ],
            ["15d5k1"],
            ["15d5k5"],
            ["15d5k10"],
            ["15d5k15"],
            ["15d5d1"],
            ["15d5d5"],
            ["15d5d10"],
            ["15d5d15"],
            ["10d5k1"],
            ["10d5k5"],
            ["10d5k10"],
            ["10d5d1"],
            ["10d5d5"],
            ["10d5d10"],
            ["20d5k1"],
            ["20d5k5"],
            ["20d5k10"],
            ["20d5k15"],
            ["20d5k20"],
            ["20d5d1"],
            ["20d5d5"],
            ["20d5d10"],
            ["20d5d15"],
            ["20d5d20"],
            ["15d6k1"],
            ["15d6k5"],
            ["15d6k10"],
            ["15d6k15"],
            ["15d6k20"],
            ["15d6d1"],
            ["15d6d5"],
            ["15d6d10"],
            ["15d6d15"],
            ["15d4k1"],
            ["15d4k5"],
            ["15d4k10"],
            ["15d4k15"],
            ["15d4d1"],
            ["15d4d5"],
            ["15d4d10"],
            ["15d4d15"],
        ]

        costs_and_times = {}
        for index, program in enumerate(programs):
            interpreter = PythonDiceInterpreter()
            cost = interpreter.get_estimated_cost(program)

            interpreter = PythonDiceInterpreter()
            start = timeit.default_timer()

            interpreter.get_probability_distributions(program)
            stop = timeit.default_timer()
            time = stop - start

            costs_and_times[index] = {"cost": cost, "time": time}

        for index, program in enumerate(programs):
            print(
                str(program),
                "|",
                costs_and_times[index]["cost"],
                "|",
                costs_and_times[index]["time"],
                flush=True,
            )
