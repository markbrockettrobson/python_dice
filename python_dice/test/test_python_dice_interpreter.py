import os
import pathlib
import unittest

import PIL.Image as Image
import PIL.ImageChops as ImageChops

import python_dice.src.python_dice_interpreter as python_dice_interpreter


class TestPythonDiceInterpreter(unittest.TestCase):
    def test_get_probability_distribution_dict(self):
        interpreter = python_dice_interpreter.PythonDiceInterpreter()
        program = [
            "VAR save_roll = d20 + 8",
            "VAR burning_arch_damage = 2d6",
            "VAR pass_save = ( save_roll >= 19 ) ",
            "VAR damage_half_on_save = burning_arch_damage // (pass_save + 1)",
        ]
        self.assertEqual(
            {
                1: 0.041666666666666664,
                2: 0.1111111111111111,
                3: 0.18055555555555555,
                4: 0.16666666666666666,
                5: 0.125,
                6: 0.08333333333333333,
                7: 0.08333333333333333,
                8: 0.06944444444444445,
                9: 0.05555555555555555,
                10: 0.041666666666666664,
                11: 0.027777777777777776,
                12: 0.013888888888888888,
            },
            interpreter.get_probability_distributions_dict(program)[
                "damage_half_on_save"
            ],
        )

    def test_get_probability_distribution(self):
        interpreter = python_dice_interpreter.PythonDiceInterpreter()
        program = [
            "VAR save_roll = d20 + 8",
            "VAR burning_arch_damage = 2d6",
            "VAR pass_save = ( save_roll >= 19 ) ",
            "VAR damage_half_on_save = burning_arch_damage // (pass_save + 1)",
        ]
        self.assertEqual(
            {
                1: 0.041666666666666664,
                2: 0.1111111111111111,
                3: 0.18055555555555555,
                4: 0.16666666666666666,
                5: 0.125,
                6: 0.08333333333333333,
                7: 0.08333333333333333,
                8: 0.06944444444444445,
                9: 0.05555555555555555,
                10: 0.041666666666666664,
                11: 0.027777777777777776,
                12: 0.013888888888888888,
            },
            interpreter.get_probability_distributions(program)[
                "damage_half_on_save"
            ].get_dict_form(),
        )

    def test_roll_single_line(self):
        interpreter = python_dice_interpreter.PythonDiceInterpreter()
        program = [
            "VAR save_roll = d20 + 8",
            "VAR burning_arch_damage = 2d6",
            "VAR pass_save = ( save_roll >= 19 ) ",
            "VAR damage_half_on_save = burning_arch_damage // (pass_save + 1)",
        ]
        out_come_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        for _ in range(1000):
            roll = interpreter.roll(program)["damage_half_on_save"]
            self.assertIn(roll, out_come_list)

    def test_min_single_line(self):
        interpreter = python_dice_interpreter.PythonDiceInterpreter()
        program = [
            "VAR save_roll = d20 + 8",
            "VAR burning_arch_damage = 2d6",
            "VAR pass_save = ( save_roll >= 19 ) ",
            "VAR damage_half_on_save = burning_arch_damage // (pass_save + 1)",
        ]
        self.assertEqual(1, interpreter.min(program)["damage_half_on_save"])

    def test_max_single_line(self):
        interpreter = python_dice_interpreter.PythonDiceInterpreter()
        program = [
            "VAR save_roll = d20 + 8",
            "VAR burning_arch_damage = 2d6",
            "VAR pass_save = ( save_roll >= 19 ) ",
            "burning_arch_damage // (pass_save + 1)",
        ]
        self.assertEqual(12, interpreter.max(program)["stdout"])

    def test_average(self):
        interpreter = python_dice_interpreter.PythonDiceInterpreter()
        program = [
            "VAR save_roll = d20 + 8",
            "VAR burning_arch_damage = 2d6",
            "VAR pass_save = ( save_roll >= 19 ) ",
            "VAR damage_half_on_save = burning_arch_damage // (pass_save + 1)",
        ]
        self.assertEqual(5.125, interpreter.get_average(program)["damage_half_on_save"])

    def disabled_test_get_histogram(self):
        interpreter = python_dice_interpreter.PythonDiceInterpreter()
        program = [
            "VAR save_roll = d20 + 8",
            "VAR burning_arch_damage = 9d6 + 9",
            "VAR pass_save = ( save_roll >= 19 ) ",
            "VAR damage_half_on_save = burning_arch_damage // (pass_save + 1)",
            "damage_half_on_save",
        ]

        image_path = pathlib.Path(
            os.path.dirname(os.path.abspath(__file__)),
            "test_image",
            "TestPythonDiceInterpreter_test_get_histogram.png",
        )
        image = interpreter.get_histogram(program)
        expected_image = Image.open(image_path)
        self.assertIsNone(ImageChops.difference(expected_image, image).getbbox())

    def disabled_test_get_at_least_histogram(self):
        interpreter = python_dice_interpreter.PythonDiceInterpreter()
        program = [
            "VAR save_roll = d20 + 8",
            "VAR burning_arch_damage = 9d6 + 9",
            "VAR pass_save = ( save_roll >= 19 ) ",
            "VAR damage_half_on_save = burning_arch_damage // (pass_save + 1)",
            "damage_half_on_save",
        ]

        image_path = pathlib.Path(
            os.path.dirname(os.path.abspath(__file__)),
            "test_image",
            "TestPythonDiceInterpreter_test_get_at_least_histogram.png",
        )
        image = interpreter.get_at_least_histogram(program)
        expected_image = Image.open(image_path)
        self.assertIsNone(ImageChops.difference(expected_image, image).getbbox())

    def disabled_test_get_at_most_histogram(self):
        interpreter = python_dice_interpreter.PythonDiceInterpreter()
        program = ["10 * 1d4"]

        image_path = pathlib.Path(
            os.path.dirname(os.path.abspath(__file__)),
            "test_image",
            "TestPythonDiceInterpreter_test_get_at_most_histogram.png",
        )
        image = interpreter.get_at_most_histogram(program)
        expected_image = Image.open(image_path)
        self.assertIsNone(ImageChops.difference(expected_image, image).getbbox())
