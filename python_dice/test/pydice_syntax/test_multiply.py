import re
import unittest
import unittest.mock as mock

import rply

import python_dice.interface.pydice_syntax.i_dice_statement as i_dice_statement
import python_dice.src.pydice_syntax.multiply as multiply


class TestAdd(unittest.TestCase):
    def setUp(self):
        self._mock_syntax = [
            mock.create_autospec(i_dice_statement.IDiceSyntax) for _ in range(2)
        ]
        self._mock_syntax[0].roll.return_value = 10
        self._mock_syntax[1].roll.return_value = 4
        self._mock_syntax[0].max.return_value = 8
        self._mock_syntax[1].max.return_value = 6
        self._mock_syntax[0].min.return_value = 2
        self._mock_syntax[1].min.return_value = 8
        self._mock_syntax[0].__str__.return_value = "7"
        self._mock_syntax[1].__str__.return_value = "2"

        self._test_add = multiply.Multiply(self._mock_syntax[0], self._mock_syntax[1])
        self._mock_parser_gen = mock.create_autospec(rply.ParserGenerator)

    def test_multiply_add_production_function(self):
        multiply.Multiply.add_production_function(self._mock_parser_gen)
        self._mock_parser_gen.production.assert_called_once_with(
            """expression : expression MULTIPLY expression"""
        )

    def test_multiply_get_token_name(self):
        self.assertEqual("MULTIPLY", self._test_add.get_token_name())
        self.assertEqual("MULTIPLY", multiply.Multiply.get_token_name())

    def test_multiply_get_token_regex(self):
        self.assertEqual(r"\*", self._test_add.get_token_regex())
        self.assertEqual(r"\*", multiply.Multiply.get_token_regex())

    def test_multiply_roll(self):
        for _ in range(100):
            self.assertEqual(40, self._test_add.roll())

    def test_multiply_max(self):
        self.assertEqual(48, self._test_add.max())

    def test_multiply_min(self):
        self.assertEqual(16, self._test_add.min())

    def test_multiply_str(self):
        self.assertEqual("7 * 2", str(self._test_add))

    def test_multiply_regex_will_match(self):
        test_cases = ["*"]
        for test_case in test_cases:
            self.assertTrue(
                re.match(multiply.Multiply.get_token_regex(), test_case),
                "did not match on case test_case %s" % test_case,
            )

    def test_multiply_regex_will_not_match(self):
        test_cases = ["a", "just a string", "", "1", " ", "-", "+", "("]
        for test_case in test_cases:
            self.assertIsNone(
                re.match(multiply.Multiply.get_token_regex(), test_case),
                "matched on case test_case %s" % test_case,
            )
