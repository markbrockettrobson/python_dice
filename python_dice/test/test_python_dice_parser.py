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
    def test_parser_constant_integer(self):
        token = self._test_parser.parse("215678284")
        self.assertEqual("CONSTANT_INTEGER", token.get_token_name())
        self.assertEqual(215678284, token.roll())
        self.assertEqual(215678284, token.max())
        self.assertEqual(215678284, token.min())
        self.assertEqual(
            {215678284: 1}, token.get_probability_distribution().get_result_map()
        )

    # pylint: disable=maybe-no-member
    def test_parser_add(self):
        token = self._test_parser.parse("3 + -20")
        self.assertEqual("ADD", token.get_token_name())
        self.assertEqual(-17, token.roll())
        self.assertEqual(-17, token.max())
        self.assertEqual(-17, token.min())
        self.assertEqual(
            {-17: 1}, token.get_probability_distribution().get_result_map()
        )

    # pylint: disable=maybe-no-member
    def test_parser_subtract(self):
        token = self._test_parser.parse("3 - -20")
        self.assertEqual("SUBTRACT", token.get_token_name())
        self.assertEqual(23, token.roll())
        self.assertEqual(23, token.max())
        self.assertEqual(23, token.min())
        self.assertEqual({23: 1}, token.get_probability_distribution().get_result_map())

    # pylint: disable=maybe-no-member
    def test_parser_add_and_subtract(self):
        token = self._test_parser.parse("3 - -20 + 2")
        self.assertEqual(25, token.roll())
        self.assertEqual(25, token.max())
        self.assertEqual(25, token.min())
        self.assertEqual({25: 1}, token.get_probability_distribution().get_result_map())

    # pylint: disable=maybe-no-member
    def test_parser_multiply(self):
        token = self._test_parser.parse("3 * -20 + 2")
        self.assertEqual(-58, token.roll())
        self.assertEqual(-58, token.max())
        self.assertEqual(-58, token.min())
        self.assertEqual(
            {-58: 1}, token.get_probability_distribution().get_result_map()
        )

    # pylint: disable=maybe-no-member
    def test_parser_multiply_order_of_operation(self):
        token = self._test_parser.parse("2 - 3 * -20")
        self.assertEqual(62, token.roll())
        self.assertEqual(62, token.max())
        self.assertEqual(62, token.min())
        self.assertEqual({62: 1}, token.get_probability_distribution().get_result_map())

    # pylint: disable=maybe-no-member
    def test_parser_integer_division(self):
        token = self._test_parser.parse("37 // 4 + 2")
        self.assertEqual(11, token.roll())
        self.assertEqual(11, token.max())
        self.assertEqual(11, token.min())
        self.assertEqual({11: 1}, token.get_probability_distribution().get_result_map())

    # pylint: disable=maybe-no-member
    def test_parser_integer_division_order_of_operation(self):
        token = self._test_parser.parse("62 // 3 * 2")
        self.assertEqual(40, token.roll())
        self.assertEqual(40, token.max())
        self.assertEqual(40, token.min())
        self.assertEqual({40: 1}, token.get_probability_distribution().get_result_map())

    # pylint: disable=maybe-no-member
    def test_parser_integer_division_order_of_operation_two(self):
        token = self._test_parser.parse("2 * 62 // 3")
        self.assertEqual(41, token.roll())
        self.assertEqual(41, token.max())
        self.assertEqual(41, token.min())
        self.assertEqual({41: 1}, token.get_probability_distribution().get_result_map())
