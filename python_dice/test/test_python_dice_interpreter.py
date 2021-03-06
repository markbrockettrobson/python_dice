import os
import pathlib
import sys
import unittest
import unittest.mock as mock

import PIL.Image as Image

import python_dice.interface.i_probability_distribution as i_probability_distribution
import python_dice.interface.i_probability_state as i_probability_state
import python_dice.interface.i_python_dice_parser as i_python_dice_parser
import python_dice.interface.python_dice_expression.i_dice_expression as i_dice_expression
import python_dice.src.python_dice_interpreter as python_dice_interpreter
import python_dice.test.pil_image_to_byte_array as pil_image_to_byte_array


class TestPythonDiceInterpreter(unittest.TestCase):
    def test_uses_given_parser(self):
        mock_expression = mock.create_autospec(i_dice_expression.IDiceExpression)
        mock_expression.max.return_value = 12

        mock_parser = mock.create_autospec(i_python_dice_parser.IPythonDiceParser)
        mock_parser.parse.return_value = (mock_expression, None)

        interpreter = python_dice_interpreter.PythonDiceInterpreter(mock_parser)
        program = ["d12"]

        self.assertEqual(12, interpreter.max(program)["stdout"])
        mock_expression.max.assert_called_once()
        mock_parser.parse.assert_called_once_with("d12", mock.ANY)

    def test_uses_starting_state(self):
        mock_probability_distribution = mock.create_autospec(
            i_probability_distribution.IProbabilityDistribution
        )
        mock_probability_distribution.get_result_map.return_value = {12: 1}

        mock_state = mock.create_autospec(
            i_probability_state.IProbabilityDistributionState
        )
        mock_state.get_var.return_value = mock_probability_distribution
        mock_state.get_constant_dict.return_value = {"stored_value": 12}

        interpreter = python_dice_interpreter.PythonDiceInterpreter(
            starting_state=mock_state
        )
        program = ["d12 + stored_value"]
        self.assertEqual(24, interpreter.max(program)["stdout"])

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
        program = ["5d2k4"]
        out_come_list = [4, 5, 6, 7, 8]
        for _ in range(1000):
            roll = interpreter.roll(program)["stdout"]
            self.assertIn(roll, out_come_list)

    def test_min_single_line(self):
        interpreter = python_dice_interpreter.PythonDiceInterpreter()
        program = ["VAR save_roll = d20 + 8"]
        self.assertEqual(9, interpreter.min(program)["save_roll"])

    def test_max_single_line(self):
        interpreter = python_dice_interpreter.PythonDiceInterpreter()
        program = ["d20 + 8"]
        self.assertEqual(28, interpreter.max(program)["stdout"])

    def test_estimated_cost_single_line(self):
        interpreter = python_dice_interpreter.PythonDiceInterpreter()
        program = ["(100d2 + 20d20k10) > 2d4"]
        self.assertEqual(4208, interpreter.get_estimated_cost(program))

    def test_average(self):
        interpreter = python_dice_interpreter.PythonDiceInterpreter()
        program = [
            "VAR save_roll = d20 + 8",
            "VAR burning_arch_damage = 2d6",
            "VAR pass_save = ( save_roll >= 19 ) ",
            "VAR damage_half_on_save = burning_arch_damage // (pass_save + 1)",
        ]
        self.assertEqual(5.125, interpreter.get_average(program)["damage_half_on_save"])

    def test_get_histogram(self):
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
            "windows" if sys.platform.startswith("win") else "linux",
            "TestPythonDiceInterpreter_test_get_histogram.tiff",
        )
        image = interpreter.get_histogram(program)
        expected_image = Image.open(image_path)
        self.assertEqual(
            pil_image_to_byte_array.image_to_byte_array(expected_image),
            pil_image_to_byte_array.image_to_byte_array(image),
        )

    def test_get_at_least_histogram(self):
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
            "windows" if sys.platform.startswith("win") else "linux",
            "TestPythonDiceInterpreter_test_get_at_least_histogram.tiff",
        )
        image = interpreter.get_at_least_histogram(program)
        expected_image = Image.open(image_path)
        self.assertEqual(
            pil_image_to_byte_array.image_to_byte_array(expected_image),
            pil_image_to_byte_array.image_to_byte_array(image),
        )

    def test_get_at_most_histogram(self):
        interpreter = python_dice_interpreter.PythonDiceInterpreter()
        program = ["10 * 1d4"]

        image_path = pathlib.Path(
            os.path.dirname(os.path.abspath(__file__)),
            "test_image",
            "windows" if sys.platform.startswith("win") else "linux",
            "TestPythonDiceInterpreter_test_get_at_most_histogram.tiff",
        )
        image = interpreter.get_at_most_histogram(program)
        expected_image = Image.open(image_path)
        self.assertEqual(
            pil_image_to_byte_array.image_to_byte_array(expected_image),
            pil_image_to_byte_array.image_to_byte_array(image),
        )

    def test_estimated_cost(self):
        interpreter = python_dice_interpreter.PythonDiceInterpreter()
        program = ["VAR a = (100d2 + 20d20k10) > 2d4", "a // 1d2"]
        self.assertEqual(4212, interpreter.get_estimated_cost(program))

    def test_probability_distribution_max(self):
        interpreter = python_dice_interpreter.PythonDiceInterpreter()
        program = ["MAX( 1d[-1, 1] , 0)"]
        probability_distribution = interpreter.get_probability_distributions(program)[
            "stdout"
        ]
        self.assertEqual({0: 0.5, 1: 0.5}, probability_distribution.get_dict_form())

    def test_probability_distribution_min(self):
        interpreter = python_dice_interpreter.PythonDiceInterpreter()
        program = ["MIN( d[-1, 1] , 0)"]
        probability_distribution = interpreter.get_probability_distributions(program)[
            "stdout"
        ]
        self.assertEqual({0: 0.5, -1: 0.5}, probability_distribution.get_dict_form())

    def test_probability_distribution_abs(self):
        interpreter = python_dice_interpreter.PythonDiceInterpreter()
        program = ["ABS( 1d[-1, 1])"]
        probability_distribution = interpreter.get_probability_distributions(program)[
            "stdout"
        ]
        self.assertEqual({1: 1}, probability_distribution.get_dict_form())

    def test_probability_distribution_add(self):
        interpreter = python_dice_interpreter.PythonDiceInterpreter()
        program = ["d[-1, 1] + 3"]
        probability_distribution = interpreter.get_probability_distributions(program)[
            "stdout"
        ]
        self.assertEqual({2: 0.5, 4: 0.5}, probability_distribution.get_dict_form())

    def test_probability_distribution_binary_operator(self):
        interpreter = python_dice_interpreter.PythonDiceInterpreter()
        operator_map = {
            "==": {0: 2, 1: 1},
            "!=": {0: 1, 1: 2},
            "<=": {1: 3},
            "<": {0: 1, 1: 2},
            ">=": {0: 2, 1: 1},
            ">": {0: 3},
            "AND": {0: 2, 1: 1},
            "OR": {1: 3},
        }
        for operator, distribution in operator_map.items():
            program = [f"d[-1-1] {operator} 1"]
            probability_distribution = interpreter.get_probability_distributions(
                program
            )["stdout"]
            self.assertEqual(distribution, probability_distribution.get_result_map())

    def test_probability_distribution_constant_binary(self):
        interpreter = python_dice_interpreter.PythonDiceInterpreter()
        program = ["2d[-1, 1]k1 == True"]
        probability_distribution = interpreter.get_probability_distributions(program)[
            "stdout"
        ]
        self.assertEqual({1: 3, 0: 1}, probability_distribution.get_result_map())

    def test_probability_distribution_var_example(self):
        interpreter = python_dice_interpreter.PythonDiceInterpreter()
        program = ["VAR a = d2", "a + 1"]
        probability_distribution = interpreter.get_probability_distributions(program)[
            "stdout"
        ]
        self.assertEqual({2: 1, 3: 1}, probability_distribution.get_result_map())

    def test_probability_distribution_div_example(self):
        interpreter = python_dice_interpreter.PythonDiceInterpreter()
        program = ["d[2,4] // 2"]
        probability_distribution = interpreter.get_probability_distributions(program)[
            "stdout"
        ]
        self.assertEqual({1: 1, 2: 1}, probability_distribution.get_result_map())

    def test_probability_distribution_multiply_example(self):
        interpreter = python_dice_interpreter.PythonDiceInterpreter()
        program = ["d[2,4] * 2"]
        probability_distribution = interpreter.get_probability_distributions(program)[
            "stdout"
        ]
        self.assertEqual({4: 1, 8: 1}, probability_distribution.get_result_map())

    def test_probability_distribution_not_example(self):
        interpreter = python_dice_interpreter.PythonDiceInterpreter()
        program = ["! (d[0,1*3])"]
        probability_distribution = interpreter.get_probability_distributions(program)[
            "stdout"
        ]
        self.assertEqual({0: 3, 1: 1}, probability_distribution.get_result_map())

    def test_probability_distribution_subtract_example(self):
        interpreter = python_dice_interpreter.PythonDiceInterpreter()
        program = ["34 - 2"]
        probability_distribution = interpreter.get_probability_distributions(program)[
            "stdout"
        ]
        self.assertEqual({32: 1}, probability_distribution.get_result_map())
