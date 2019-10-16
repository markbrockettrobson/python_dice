import unittest
import unittest.mock as mock

import python_dice.src.python_dice_lexer as pydice_lexer
import python_dice.src.python_dice_parser as pydice_parser


class TestPythonDiceParser(unittest.TestCase):
    def setUp(self):
        self._test_parser = pydice_parser.PythonDiceParser()
        self._mock_pydice_lexer = mock.create_autospec(pydice_lexer.PythonDiceLexer)
        self._mock_token_iter = iter(pydice_lexer.PythonDiceLexer().lex("3"))
        self._mock_pydice_lexer.lex.return_value = self._mock_token_iter

    def test_use_injected_lexer(self):
        self._test_parser = pydice_parser.PythonDiceParser(self._mock_pydice_lexer)
        self._test_parser.parse("215678284")
        self._mock_pydice_lexer.lex.assert_called_once_with("215678284")

    # pylint: disable=maybe-no-member
    def assert_distribution(self, token, expected_outcome, min_value, max_value):
        for _ in range(1000):
            self.assertIn(token.roll(), expected_outcome.keys())
        self.assertEqual(max_value, token.max())
        self.assertEqual(min_value, token.min())
        self.assertEqual(
            expected_outcome, token.get_probability_distribution().get_result_map()
        )

    def test_parser_constant_integer(self):
        token = self._test_parser.parse("215678284")
        expected_outcome = {215678284: 1}
        self.assert_distribution(token, expected_outcome, 215678284, 215678284)

    def test_parser_add(self):
        token = self._test_parser.parse("3 + -20")
        expected_outcome = {-17: 1}
        self.assert_distribution(token, expected_outcome, -17, -17)

    def test_parser_subtract(self):
        token = self._test_parser.parse("3 - -20")
        expected_outcome = {23: 1}
        self.assert_distribution(token, expected_outcome, 23, 23)

    def test_parser_add_and_subtract(self):
        token = self._test_parser.parse("3 - -20 + 2")
        expected_outcome = {25: 1}
        self.assert_distribution(token, expected_outcome, 25, 25)

    def test_parser_multiply(self):
        token = self._test_parser.parse("3 * -20 + 2")
        expected_outcome = {-58: 1}
        self.assert_distribution(token, expected_outcome, -58, -58)

    def test_parser_multiply_order_of_operation(self):
        token = self._test_parser.parse("2 - 3 * -20")
        expected_outcome = {62: 1}
        self.assert_distribution(token, expected_outcome, 62, 62)

    def test_parser_integer_division(self):
        token = self._test_parser.parse("37 // 4 + 2")
        expected_outcome = {11: 1}
        self.assert_distribution(token, expected_outcome, 11, 11)

    def test_parser_integer_division_order_of_operation(self):
        token = self._test_parser.parse("62 // 3 * 2")
        expected_outcome = {40: 1}
        self.assert_distribution(token, expected_outcome, 40, 40)

    def test_parser_integer_division_order_of_operation_two(self):
        token = self._test_parser.parse("2 * 62 // 3")
        expected_outcome = {41: 1}
        self.assert_distribution(token, expected_outcome, 41, 41)

    def test_parser_dice(self):
        token = self._test_parser.parse("2d4 * 2 // 3")
        expected_outcome = {1: 1, 2: 5, 3: 4, 4: 5, 5: 1}
        self.assert_distribution(token, expected_outcome, 1, 5)

    def test_parser_dice_add(self):
        token = self._test_parser.parse("2d4 + 1d2")
        expected_outcome = {3: 1, 4: 3, 5: 5, 6: 7, 7: 7, 8: 5, 9: 3, 10: 1}
        self.assert_distribution(token, expected_outcome, 3, 10)

    def test_parser_dice_subtract(self):
        token = self._test_parser.parse("2d4 - 1d2")
        expected_outcome = {0: 1, 1: 3, 2: 5, 3: 7, 4: 7, 5: 5, 6: 3, 7: 1}
        self.assert_distribution(token, expected_outcome, 0, 7)

    def test_parser_dice_multiply(self):
        token = self._test_parser.parse("2d4 * 1d2")
        expected_outcome = {
            2: 1,
            4: 4,
            3: 2,
            6: 5,
            8: 4,
            5: 4,
            10: 4,
            12: 3,
            7: 2,
            14: 2,
            16: 1,
        }
        self.assert_distribution(token, expected_outcome, 2, 16)

    def test_parser_dice_division(self):
        token = self._test_parser.parse("2d4 // 1d2")
        expected_outcome = {2: 8, 1: 3, 3: 7, 4: 4, 5: 4, 6: 3, 7: 2, 8: 1}
        self.assert_distribution(token, expected_outcome, 1, 8)

    def test_parser_dice_full_test(self):
        token = self._test_parser.parse("2d4 * 1d2 + 6d6 // 1d4")
        expected_outcome = {
            8: 150534,
            5: 5474,
            4: 497,
            3: 7,
            9: 242121,
            10: 322235,
            6: 25810,
            11: 369126,
            12: 382604,
            7: 73494,
            13: 375640,
            14: 363690,
            15: 353106,
            16: 335747,
            17: 311542,
            18: 281505,
            19: 250023,
            20: 220599,
            21: 195160,
            22: 172718,
            23: 154828,
            24: 143472,
            25: 135890,
            26: 130051,
            27: 124406,
            28: 117875,
            29: 110298,
            30: 101872,
            31: 92682,
            32: 82787,
            33: 72395,
            34: 61864,
            35: 51618,
            36: 42025,
            37: 33348,
            38: 25747,
            39: 19290,
            40: 13981,
            41: 9764,
            42: 6542,
            43: 4184,
            44: 2539,
            45: 1452,
            46: 775,
            47: 382,
            48: 171,
            49: 68,
            50: 23,
            51: 6,
            52: 1,
        }
        self.assert_distribution(token, expected_outcome, 3, 52)

    def test_parser_parenthesis_enclosed_expression(self):
        token = self._test_parser.parse("(1d4 + 2 )// 1d2")
        expected_outcome = {1: 1, 2: 2, 3: 2, 4: 1, 5: 1, 6: 1}
        self.assert_distribution(token, expected_outcome, 1, 6)

    def test_parser_constant_binary_expression(self):
        token = self._test_parser.parse("True + True - (False * 2d6)")
        expected_outcome = {2: 36}
        self.assert_distribution(token, expected_outcome, 2, 2)

    def test_parser_not_expression(self):
        token = self._test_parser.parse("!(1d6 - 1d6)")
        expected_outcome = {0: 30, 1: 6}
        self.assert_distribution(token, expected_outcome, 0, 1)

    def test_parser_equal_expression(self):
        token = self._test_parser.parse("1d6 == 1d6")
        expected_outcome = {0: 30, 1: 6}
        self.assert_distribution(token, expected_outcome, 0, 1)

    def test_parser_not_equal_expression(self):
        token = self._test_parser.parse("1d6 != 3")
        expected_outcome = {0: 1, 1: 5}
        self.assert_distribution(token, expected_outcome, 0, 1)

    def test_parser_less_than_equal_expression(self):
        token = self._test_parser.parse("((8d6 + 8) // 2) >= (2d8 + 5)")
        expected_outcome = {0: 16394638, 1: 91100786}
        self.assert_distribution(token, expected_outcome, 0, 1)

    def test_parser_less_than_expression(self):
        token = self._test_parser.parse("((8d6 + 8) // 2) > (3d8 + 5)")
        expected_outcome = {0: 518536200, 1: 341427192}
        self.assert_distribution(token, expected_outcome, 0, 1)

    def test_parser_greater_than_equal_expression(self):
        token = self._test_parser.parse("((8d6 + 8) // 2) <= (3d8 + 5)")
        expected_outcome = {0: 341427192, 1: 518536200}
        self.assert_distribution(token, expected_outcome, 0, 1)

    def test_parser_greater_than_expression(self):
        token = self._test_parser.parse("((8d6 + 8) // 2) < (2d8 + 5)")
        expected_outcome = {0: 91100786, 1: 16394638}
        self.assert_distribution(token, expected_outcome, 0, 1)

    def test_parser_and_expression(self):
        token = self._test_parser.parse(
            "(((1d2 == 2) AND ((1d20 + 6) >= 22))) > ((1d20 + 6) >= 23)"
        )
        expected_outcome = {0: 720, 1: 80}
        self.assert_distribution(token, expected_outcome, 0, 1)

    def test_parser_or_expression(self):
        token = self._test_parser.parse("((1d20 + 7) > 19) OR ((1d20 + 7) > 19)")
        expected_outcome = {0: 144, 1: 256}
        self.assert_distribution(token, expected_outcome, 0, 1)

    def test_parser_max_expression(self):
        token = self._test_parser.parse("MAX(1d20 + 3, 1d20 + 3) > 15")
        expected_outcome = {0: 144, 1: 256}
        self.assert_distribution(token, expected_outcome, 0, 1)

    def test_parser_min_expression(self):
        token = self._test_parser.parse("MIN(1d20 + 3, 1d20 + 3) > 15")
        expected_outcome = {0: 336, 1: 64}
        self.assert_distribution(token, expected_outcome, 0, 1)

    def test_parser_abs_expression(self):
        token = self._test_parser.parse("ABS(1d4 - 1d4)")
        expected_outcome = {0: 4, 1: 6, 2: 4, 3: 2}
        self.assert_distribution(token, expected_outcome, 0, 3)
