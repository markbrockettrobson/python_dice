import unittest
import unittest.mock as mock

import rply

import python_dice.src.python_dice_expression.constant_binary_expression as constant_binary_expression


class TestConstantIntegerExpression(unittest.TestCase):
    def setUp(self):
        self._test_constant_binary_true = constant_binary_expression.ConstantBinaryExpression(
            "True"
        )
        self._test_constant_binary_false = constant_binary_expression.ConstantBinaryExpression(
            "False"
        )
        self._mock_parser_gen = mock.create_autospec(rply.ParserGenerator)

    def test_constant_binary_add_production_function(self):
        constant_binary_expression.ConstantBinaryExpression.add_production_function(
            self._mock_parser_gen
        )
        self._mock_parser_gen.production.assert_called_once_with(
            """expression : CONSTANT_BINARY"""
        )

    def test_constant_binary_roll(self):
        for _ in range(100):
            self.assertEqual(1, self._test_constant_binary_true.roll())
            self.assertEqual(0, self._test_constant_binary_false.roll())

    def test_constant_binary_max(self):
        self.assertEqual(1, self._test_constant_binary_true.max())
        self.assertEqual(0, self._test_constant_binary_false.max())

    def test_constant_binary_min(self):
        self.assertEqual(1, self._test_constant_binary_true.min())
        self.assertEqual(0, self._test_constant_binary_false.min())

    def test_constant_binary_str(self):
        self.assertEqual("True", str(self._test_constant_binary_true))
        self.assertEqual("False", str(self._test_constant_binary_false))

    def test_constant_binary_get_probability_distribution(self):
        self.assertEqual(
            {1: 1},
            self._test_constant_binary_true.get_probability_distribution().get_result_map(),
        )
        self.assertEqual(
            {0: 1},
            self._test_constant_binary_false.get_probability_distribution().get_result_map(),
        )
