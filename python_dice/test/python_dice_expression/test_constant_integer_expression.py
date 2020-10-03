import unittest
import unittest.mock as mock

import rply

import python_dice.src.python_dice_expression.constant_integer_expression as constant_integer_expression


class TestConstantIntegerExpression(unittest.TestCase):
    def setUp(self):
        self._test_constant_integers = (
            constant_integer_expression.ConstantIntegerExpression("14")
        )
        self._mock_parser_gen = mock.create_autospec(rply.ParserGenerator)

    def test_constant_integer_add_production_function(self):
        constant_integer_expression.ConstantIntegerExpression.add_production_function(
            self._mock_parser_gen
        )
        self._mock_parser_gen.production.assert_called_once_with(
            """expression : CONSTANT_INTEGER"""
        )

    def test_constant_integer_roll(self):
        for _ in range(100):
            self.assertEqual(14, self._test_constant_integers.roll())

    def test_constant_integer_max(self):
        self.assertEqual(14, self._test_constant_integers.max())

    def test_constant_integer_min(self):
        self.assertEqual(14, self._test_constant_integers.min())

    def test_constant_integer_str(self):
        self.assertEqual("14", str(self._test_constant_integers))

    def test_constant_integer_estimated_cost(self):
        self.assertEqual(1, self._test_constant_integers.estimated_cost())

    def test_constant_integer_probability_distribution(self):
        self.assertEqual(
            {14: 1},
            self._test_constant_integers.get_probability_distribution().get_result_map(),
        )
