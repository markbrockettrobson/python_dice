from unittest import TestCase
from unittest.mock import ANY, create_autospec

from PIL import Image  # type: ignore

from python_dice.interface.expression.i_dice_expression import IDiceExpression
from python_dice.interface.i_python_dice_parser import IPythonDiceParser
from python_dice.interface.probability_distribution.i_probability_distribution_state import (
    IProbabilityDistributionState,
)
from python_dice.src.python_dice_interpreter import PythonDiceInterpreter
from python_dice.test import pil_image_to_byte_array

# pylint: disable=too-many-public-methods
from python_dice.test.test_image.test_image_path_finder import get_image_path


class TestPythonDiceInterpreter(TestCase):
    def test_uses_given_parser(self):
        mock_expression = create_autospec(IDiceExpression)
        mock_expression.max.return_value = 12

        mock_parser = create_autospec(IPythonDiceParser)
        mock_parser.parse.return_value = (mock_expression, None)

        interpreter = PythonDiceInterpreter(mock_parser)
        program = ["d12"]

        self.assertEqual(12, interpreter.max(program)["stdout"])
        mock_expression.max.assert_called_once()
        mock_parser.parse.assert_called_once_with("d12", ANY)

    def test_uses_starting_state(self):
        test_interpreter_one = PythonDiceInterpreter()
        probability_distribution = test_interpreter_one.get_probability_distributions(["d12"])["stdout"]

        mock_state = create_autospec(IProbabilityDistributionState)
        mock_state.get_var.return_value = probability_distribution
        mock_state.get_constant_dict.return_value = {"stored_value": 12}

        interpreter = PythonDiceInterpreter(starting_state=mock_state)
        program = ["d12 + stored_value"]
        self.assertEqual(24, interpreter.max(program)["stdout"])

    def test_get_probability_distribution_dict(self):
        interpreter = PythonDiceInterpreter()
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
            interpreter.get_probability_distributions_dict(program)["damage_half_on_save"],
        )

    def test_get_probability_distribution(self):
        interpreter = PythonDiceInterpreter()
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
            interpreter.get_probability_distributions(program)["damage_half_on_save"].get_dict_form(),
        )

    def test_roll_single_line(self):
        interpreter = PythonDiceInterpreter()
        program = ["5d2k4"]
        out_come_list = [4, 5, 6, 7, 8]
        for _ in range(1000):
            roll = interpreter.roll(program)["stdout"]
            self.assertIn(roll, out_come_list)

    def test_min_single_line(self):
        interpreter = PythonDiceInterpreter()
        program = ["VAR save_roll = d20 + 8"]
        self.assertEqual(9, interpreter.min(program)["save_roll"])

    def test_max_single_line(self):
        interpreter = PythonDiceInterpreter()
        program = ["d20 + 8"]
        self.assertEqual(28, interpreter.max(program)["stdout"])

    def test_estimated_cost_single_line(self):
        interpreter = PythonDiceInterpreter()
        program = ["(100d2 + 20d20k10) > 2d4"]
        self.assertEqual(4208, interpreter.get_estimated_cost(program))

    def test_average(self):
        interpreter = PythonDiceInterpreter()
        program = [
            "VAR save_roll = d20 + 8",
            "VAR burning_arch_damage = 2d6",
            "VAR pass_save = ( save_roll >= 19 ) ",
            "VAR damage_half_on_save = burning_arch_damage // (pass_save + 1)",
        ]
        self.assertEqual(5.125, interpreter.get_average(program)["damage_half_on_save"])

    def test_get_histogram(self):
        interpreter = PythonDiceInterpreter()
        program = [
            "VAR save_roll = d20 + 8",
            "VAR burning_arch_damage = 9d6 + 9",
            "VAR pass_save = ( save_roll >= 19 ) ",
            "VAR damage_half_on_save = burning_arch_damage // (pass_save + 1)",
            "damage_half_on_save",
        ]

        image_path = get_image_path(
            "TestPythonDiceInterpreter_test_get_histogram.tiff",
        )
        image = interpreter.get_histogram(program)
        expected_image = Image.open(image_path)
        self.assertEqual(
            pil_image_to_byte_array.image_to_byte_array(expected_image),
            pil_image_to_byte_array.image_to_byte_array(image),
        )

    def test_get_at_least_histogram(self):
        interpreter = PythonDiceInterpreter()
        program = [
            "VAR save_roll = d20 + 8",
            "VAR burning_arch_damage = 9d6 + 9",
            "VAR pass_save = ( save_roll >= 19 ) ",
            "VAR damage_half_on_save = burning_arch_damage // (pass_save + 1)",
            "damage_half_on_save",
        ]

        image_path = get_image_path(
            "TestPythonDiceInterpreter_test_get_at_least_histogram.tiff",
        )
        image = interpreter.get_at_least_histogram(program)
        expected_image = Image.open(image_path)
        self.assertEqual(
            pil_image_to_byte_array.image_to_byte_array(expected_image),
            pil_image_to_byte_array.image_to_byte_array(image),
        )

    def test_get_at_most_histogram(self):
        interpreter = PythonDiceInterpreter()
        program = ["10 * 1d4"]

        image_path = get_image_path(
            "TestPythonDiceInterpreter_test_get_at_most_histogram.tiff",
        )
        image = interpreter.get_at_most_histogram(program)
        expected_image = Image.open(image_path)
        self.assertEqual(
            pil_image_to_byte_array.image_to_byte_array(expected_image),
            pil_image_to_byte_array.image_to_byte_array(image),
        )

    def test_estimated_cost(self):
        subtest = [
            (["1d20"], 20),
            (["2d20"], 40),
            (["2d20k1"], 40),
            (["3d20k2"], 60 * 2),
            (["10d[1--2]"], 40),
            (["10d[1--2]k2"], 80),
            (["VAR a = 1d10", "a"], 22),
            (["VAR a = 1d10", "VAR b = 1d10", "a + b"], 12 + 12 + 20),
            (["VAR a = 1d10", "VAR b = 1d10 + a", "VAR a = 1d20"], 12 + 22 + 22),
            (["VAR a = (100d2 + 20d20k10) > 2d4", "a // 1d2"], 8420),
        ]

        for program, expected_cost in subtest:
            with self.subTest("~".join(program)):
                interpreter = PythonDiceInterpreter()
                self.assertEqual(interpreter.get_estimated_cost(program), expected_cost)

    def test_probability_distribution_max(self):
        interpreter = PythonDiceInterpreter()
        program = ["MAX( 1d[-1, 1] , 0)"]
        probability_distribution = interpreter.get_probability_distributions(program)["stdout"]
        self.assertEqual({0: 0.5, 1: 0.5}, probability_distribution.get_dict_form())

    def test_probability_distribution_min(self):
        interpreter = PythonDiceInterpreter()
        program = ["MIN( d[-1, 1] , 0)"]
        probability_distribution = interpreter.get_probability_distributions(program)["stdout"]
        self.assertEqual({0: 0.5, -1: 0.5}, probability_distribution.get_dict_form())

    def test_probability_distribution_abs(self):
        interpreter = PythonDiceInterpreter()
        program = ["ABS( 1d[-1, 1])"]
        probability_distribution = interpreter.get_probability_distributions(program)["stdout"]
        self.assertEqual({1: 1}, probability_distribution.get_dict_form())

    def test_probability_distribution_add(self):
        interpreter = PythonDiceInterpreter()
        program = ["d[-1, 1] + 3"]
        probability_distribution = interpreter.get_probability_distributions(program)["stdout"]
        self.assertEqual({2: 0.5, 4: 0.5}, probability_distribution.get_dict_form())

    def test_probability_distribution_binary_operator(self):
        interpreter = PythonDiceInterpreter()
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
            probability_distribution = interpreter.get_probability_distributions(program)["stdout"]
            self.assertEqual(distribution, probability_distribution.get_result_map())

    def test_probability_distribution_constant_binary(self):
        interpreter = PythonDiceInterpreter()
        program = ["2d[-1, 1]k1 == True"]
        probability_distribution = interpreter.get_probability_distributions(program)["stdout"]
        self.assertEqual({1: 3, 0: 1}, probability_distribution.get_result_map())

    def test_probability_distribution_var_example(self):
        interpreter = PythonDiceInterpreter()
        program = ["VAR a = d2", "a + 1"]
        probability_distribution = interpreter.get_probability_distributions(program)["stdout"]
        self.assertEqual({2: 1, 3: 1}, probability_distribution.get_result_map())

    def test_probability_distribution_div_example(self):
        interpreter = PythonDiceInterpreter()
        program = ["d[2,4] // 2"]
        probability_distribution = interpreter.get_probability_distributions(program)["stdout"]
        self.assertEqual({1: 1, 2: 1}, probability_distribution.get_result_map())

    def test_probability_distribution_multiply_example(self):
        interpreter = PythonDiceInterpreter()
        program = ["d[2,4] * 2"]
        probability_distribution = interpreter.get_probability_distributions(program)["stdout"]
        self.assertEqual({4: 1, 8: 1}, probability_distribution.get_result_map())

    def test_probability_distribution_not_example(self):
        interpreter = PythonDiceInterpreter()
        program = ["! (d[0,1*3])"]
        probability_distribution = interpreter.get_probability_distributions(program)["stdout"]
        self.assertEqual({0: 3, 1: 1}, probability_distribution.get_result_map())

    def test_probability_distribution_subtract_example(self):
        interpreter = PythonDiceInterpreter()
        program = ["34 - 2"]
        probability_distribution = interpreter.get_probability_distributions(program)["stdout"]
        self.assertEqual({32: 1}, probability_distribution.get_result_map())

    def test_probability_distribution_two_entangled_variables_example(self):
        interpreter = PythonDiceInterpreter()
        program = [
            "VAR roll_one = 1d3",
            "VAR roll_two = ((1d4) * (roll_one == 3)) + ((roll_one) * (roll_one != 3))",
            "roll_two",
        ]
        probability_distribution = interpreter.get_probability_distributions(program)["stdout"]
        self.assertEqual(
            {
                1: 5,
                2: 5,
                3: 1,
                4: 1,
            },
            probability_distribution.get_result_map(),
        )

    def test_probability_distribution_three_entangled_variables_example(self):
        interpreter = PythonDiceInterpreter()
        program = [
            "VAR roll_one = 1d3",
            "VAR roll_two = ((1d4) * (roll_one == 3)) + ((roll_one) * (roll_one != 3))",
            "VAR roll_three = ((1d5) * (roll_two == 4)) + ((roll_two) * (roll_two != 4))",
            "roll_three",
        ]
        probability_distribution = interpreter.get_probability_distributions(program)["stdout"]
        self.assertEqual(
            {
                1: 326,
                2: 326,
                3: 6,
                4: 1,
                5: 1,
            },
            probability_distribution.get_result_map(),
        )

    def test_probability_distribution_two_entangled_variables_renamed(self):
        interpreter = PythonDiceInterpreter()
        program = [
            "VAR a = 1d2",
            "VAR b = a + a",
            "VAR c = a + b",
            "VAR d = c >= ( 1d2 * b )",
            "VAR e = d == a",
        ]
        probability_distribution_a = interpreter.get_probability_distributions(program)["a"]
        probability_distribution_b = interpreter.get_probability_distributions(program)["b"]
        probability_distribution_c = interpreter.get_probability_distributions(program)["c"]
        probability_distribution_d = interpreter.get_probability_distributions(program)["d"]
        probability_distribution_e = interpreter.get_probability_distributions(program)["e"]

        self.assertEqual(
            {
                1: 1,
                2: 1,
            },
            probability_distribution_a.get_result_map(),
        )
        self.assertEqual(
            {
                2: 1,
                4: 1,
            },
            probability_distribution_b.get_result_map(),
        )
        self.assertEqual(
            {
                3: 1,
                6: 1,
            },
            probability_distribution_c.get_result_map(),
        )
        self.assertEqual(
            {
                0: 2,
                1: 2,
            },
            probability_distribution_d.get_result_map(),
        )
        self.assertEqual(
            {
                0: 3,
                1: 1,
            },
            probability_distribution_e.get_result_map(),
        )

    def test_probability_distribution_two_entangled_variables_simple(self):
        interpreter = PythonDiceInterpreter()
        program = [
            "VAR a = 2d3",
            "VAR b = a + a",
        ]
        probability_distribution_b = interpreter.get_probability_distributions(program)["b"]
        self.assertEqual(
            {
                4: 1,
                6: 4,
                8: 9,
                10: 4,
                12: 1,
            },
            probability_distribution_b.get_result_map(),
        )

    def test_probability_distribution_two_entangled_variables_chain(self):
        interpreter = PythonDiceInterpreter()
        program = [
            "VAR a = 2d3",
            "VAR b = a + a",
            "VAR a = b + a",
            "VAR b = b + a",
        ]
        probability_distribution_b = interpreter.get_probability_distributions(program)["b"]
        self.assertEqual(
            {
                10: 1,
                15: 32,
                20: 243,
                25: 32,
                30: 1,
            },
            probability_distribution_b.get_result_map(),
        )

    def test_probability_distribution_fixed_value_partly_entangled(self):
        interpreter = PythonDiceInterpreter()
        program = [
            "VAR a = 1d4",
            "VAR b = a>=3",
            "VAR c = a>=4",
            "VAR d = 1*b",
            "VAR e = (10-d)*c",
            "VAR out = d+e"
        ]
        probability_distribution_b = interpreter.get_probability_distributions(program)["out"]
        print(probability_distribution_b)
        self.assertEqual(
            {
                0: 2,
                1: 1,
                10: 1,
            },
            probability_distribution_b.get_result_map(),
        )

    def test_probability_distribution_random_value_partly_entangled(self):
        interpreter = PythonDiceInterpreter()
        program = [
            "VAR a = 1d4",
            "VAR b = a>=3",
            "VAR c = a>=4",
            "VAR d = 1d2*b",
            "VAR e = (10-d)*c",
            "VAR out = d+e"
        ]
        probability_distribution_b = interpreter.get_probability_distributions(program)["out"]
        print(probability_distribution_b)
        self.assertEqual(
            {
                0: 4,
                1: 1,
                2: 1,
                10: 2,
            },
            probability_distribution_b.get_result_map(),
        )

    def test_probability_distribution_many_random_value_partly_entangled(self):
        interpreter = PythonDiceInterpreter()
        program = [
            "VAR a = 1d4",
            "VAR b = a>=2*1d2",
            "VAR c = a>=3*1d[10,20]",
            "VAR d = a>=4*1d[100,200]",
            "VAR out = b+c+d"
        ]
        probability_distribution_b = interpreter.get_probability_distributions(program)["out"]
        print(probability_distribution_b)
        self.assertEqual(
            {
                0: 8,
                1: 4,
                2: 4,
                11: 2,
                12: 2,
                21: 2,
                22: 2,
                111: 1,
                112: 1,
                121: 1,
                122: 1,
                211: 1,
                212: 1,
                221: 1,
                222: 1,
            },
            probability_distribution_b.get_result_map(),
        )

    def test_probability_distribution_many_random_value_partly_entangled_with_loop(self):
        interpreter = PythonDiceInterpreter()
        program = [
            "VAR a = 1d4",
            "VAR b = a>=2*1d2",
            "VAR c = a>=3*b*10",
            "VAR d = a>=4*c*10",
            "VAR out = b+c+d"
        ]
        probability_distribution_b = interpreter.get_probability_distributions(program)["out"]
        print(probability_distribution_b)
        self.assertEqual(
            {
                0: 8,
                1: 4,
                2: 4,
                11: 4,
                22: 4,
                111: 4,
                222: 4,
            },
            probability_distribution_b.get_result_map(),
        )

    def test_probability_distribution_many_random_value_partly_entangled_with_loop_example_two(self):
        interpreter = PythonDiceInterpreter()
        program = [
            "VAR a = 1d4",
            "VAR b = a>=2*1d2",
            "VAR c = a>=3*b*10",
            "VAR out = b+c"
        ]
        probability_distribution_b = interpreter.get_probability_distributions(program)["out"]
        print(probability_distribution_b)
        self.assertEqual(
            {
                0: 4,
                1: 2,
                2: 2,
                11: 2,
                22: 2,
            },
            probability_distribution_b.get_result_map(),
        )

    def test_probability_distribution_many_random_value_partly_entangled_with_loop_example_three(self):
        interpreter = PythonDiceInterpreter()
        program = [
            "VAR a = 1d4",
            "VAR b = a>=2*1d2",
            "VAR c = a>=3*b*b*10",
        ]
        probability_distribution_b = interpreter.get_probability_distributions(program)["c"]
        print(probability_distribution_b)
        self.assertEqual(
            {
                0: 4,
                10: 2,
                40: 2,
            },
            probability_distribution_b.get_result_map(),
        )

    def test_probability_distribution_many_random_value_partly_entangled_small_example(self):
        interpreter = PythonDiceInterpreter()
        program = [
            "VAR a = 1d2",
            "VAR b = a+a*d[10,20]",
        ]
        probability_distribution_b = interpreter.get_probability_distributions(program)["b"]
        print(probability_distribution_b)
        self.assertEqual(
            {
                11: 1,
                21: 1,
                22: 1,
                42: 1,
            },
            probability_distribution_b.get_result_map(),
        )
 
    def test_probability_distribution_many_random_value_partly_entangled_small_example_two(self):
        interpreter = PythonDiceInterpreter()
        program = [
            "VAR a = 1d2",
            "VAR b = a>=2*a+a",
        ]
        probability_distribution_b = interpreter.get_probability_distributions(program)["b"]
        print(probability_distribution_b)
        self.assertEqual(
            {
                1: 1,
                4: 1,
            },
            probability_distribution_b.get_result_map(),
        )
 