import unittest

import python_dice.src.python_dice_interpreter as python_dice_interpreter


class TestPythonDiceInterpreter(unittest.TestCase):
    def test_get_probability_distribution(self):
        interpreter = python_dice_interpreter.PythonDiceInterpreter()
        program = [
            "VAR save_roll = 1d20 + 8",
            "VAR burning_arch_damage = 2d6",
            "VAR pass_save = ( save_roll >= 19 ) ",
            "VAR damage_half_on_save = burning_arch_damage // (pass_save + 1)",
        ]
        self.assertEqual(
            {
                2: 80,
                1: 30,
                3: 130,
                4: 120,
                5: 90,
                6: 60,
                7: 60,
                8: 50,
                9: 40,
                10: 30,
                11: 20,
                12: 10,
            },
            interpreter.get_probability_distribution(program)
            .get_var("damage_half_on_save")
            .get_result_map(),
        )

    def test_roll_single_line(self):
        interpreter = python_dice_interpreter.PythonDiceInterpreter()
        program = [
            "VAR save_roll = 1d20 + 8",
            "VAR burning_arch_damage = 2d6",
            "VAR pass_save = ( save_roll >= 19 ) ",
            "VAR damage_half_on_save = burning_arch_damage // (pass_save + 1)",
        ]
        out_come_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        for _ in range(1000):
            roll = interpreter.roll(program).get_constant("damage_half_on_save")
            self.assertIn(roll, out_come_list)

    def test_min_single_line(self):
        interpreter = python_dice_interpreter.PythonDiceInterpreter()
        program = [
            "VAR save_roll = 1d20 + 8",
            "VAR burning_arch_damage = 2d6",
            "VAR pass_save = ( save_roll >= 19 ) ",
            "VAR damage_half_on_save = burning_arch_damage // (pass_save + 1)",
        ]
        self.assertEqual(
            1, interpreter.min(program).get_constant("damage_half_on_save")
        )

    def test_max_single_line(self):
        interpreter = python_dice_interpreter.PythonDiceInterpreter()
        program = [
            "VAR save_roll = 1d20 + 8",
            "VAR burning_arch_damage = 2d6",
            "VAR pass_save = ( save_roll >= 19 ) ",
            "VAR damage_half_on_save = burning_arch_damage // (pass_save + 1)",
        ]
        self.assertEqual(
            12, interpreter.max(program).get_constant("damage_half_on_save")
        )
