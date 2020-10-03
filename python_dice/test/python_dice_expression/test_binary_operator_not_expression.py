import unittest
import unittest.mock as mock

import rply

import python_dice.interface.python_dice_expression.i_dice_expression as i_dice_expression
import python_dice.src.probability_distribution as probability_distribution
import python_dice.src.python_dice_expression.not_expression as not_expression


class TestBinaryOperatorNotExpression(unittest.TestCase):
    def setUp(self):
        self._mock_syntax = mock.create_autospec(i_dice_expression.IDiceExpression)
        self._mock_syntax.roll.return_value = 0
        self._mock_syntax.max.return_value = 8
        self._mock_syntax.min.return_value = 6
        self._mock_syntax.__str__.return_value = "7d3"
        self._mock_syntax.estimated_cost.return_value = 9
        self._mock_syntax.get_probability_distribution.return_value = probability_distribution.ProbabilityDistribution(
            {-3: 1, 0: 2, 4: 1}
        )

        self._test_binary_operator = not_expression.NotExpression(self._mock_syntax)
        self._mock_parser_gen = mock.create_autospec(rply.ParserGenerator)

    def test_binary_operator_add_production_function(self):
        not_expression.NotExpression.add_production_function(self._mock_parser_gen)
        self._mock_parser_gen.production.assert_called_once_with(
            """expression : NOT expression"""
        )

    def test_ne_roll_true(self):
        for _ in range(100):
            self.assertEqual(1, self._test_binary_operator.roll())

    def test_ne_roll_false(self):
        self._mock_syntax.roll.return_value = 4
        for _ in range(100):
            self.assertEqual(0, self._test_binary_operator.roll())

    def test_ne_max_true(self):
        self._mock_syntax.max.return_value = 4
        self.assertEqual(1, self._test_binary_operator.max())

    def test_ne_max_false(self):
        self._mock_syntax.get_probability_distribution.return_value = probability_distribution.ProbabilityDistribution(
            {4: 1, 54: 1}
        )
        self.assertEqual(0, self._test_binary_operator.max())

    def test_ne_min_true(self):
        self._mock_syntax.get_probability_distribution.return_value = probability_distribution.ProbabilityDistribution(
            {0: 1}
        )
        self.assertEqual(1, self._test_binary_operator.min())

    def test_ne_min_false(self):
        self.assertEqual(0, self._test_binary_operator.min())

    def test_ne_str(self):
        self.assertEqual("!7d3", str(self._test_binary_operator))

    def test_ne_estimated_cost(self):
        self.assertEqual(9, self._test_binary_operator.estimated_cost())

    def test_ne_get_probability_distribution(self):
        self.assertEqual(
            {0: 2, 1: 2},
            self._test_binary_operator.get_probability_distribution().get_result_map(),
        )
