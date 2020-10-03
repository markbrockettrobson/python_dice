import unittest
import unittest.mock as mock

import rply

import python_dice.interface.python_dice_expression.i_dice_expression as i_dice_expression
import python_dice.src.probability_distribution as probability_distribution
import python_dice.src.python_dice_expression.abs_expression as abs_expression


class TestAbsExpression(unittest.TestCase):
    def setUp(self):
        self._mock_syntax = mock.create_autospec(i_dice_expression.IDiceExpression)
        self._mock_syntax.roll.return_value = 2
        self._mock_syntax.max.return_value = 8
        self._mock_syntax.min.return_value = 6
        self._mock_syntax.__str__.return_value = "7d3"
        self._mock_syntax.estimated_cost.return_value = 21
        self._mock_syntax.get_probability_distribution.return_value = (
            probability_distribution.ProbabilityDistribution({-5: 1, 1: 2, 4: 1})
        )

        self._test_abs_operator = abs_expression.AbsExpression(self._mock_syntax)
        self._mock_parser_gen = mock.create_autospec(rply.ParserGenerator)

    def test_abs_add_production_function(self):
        abs_expression.AbsExpression.add_production_function(self._mock_parser_gen)
        self._mock_parser_gen.production.assert_called_once_with(
            """expression : ABS OPEN_PARENTHESIS expression CLOSE_PARENTHESIS"""
        )

    def test_abs_roll_pos(self):
        for _ in range(100):
            self.assertEqual(2, self._test_abs_operator.roll())

    def test_abs_roll_neg(self):
        self._mock_syntax.roll.return_value = -4
        for _ in range(100):
            self.assertEqual(4, self._test_abs_operator.roll())

    def test_abs_max(self):
        self.assertEqual(5, self._test_abs_operator.max())

    def test_abs_min(self):
        self.assertEqual(1, self._test_abs_operator.min())

    def test_abs_str(self):
        self.assertEqual("ABS(7d3)", str(self._test_abs_operator))

    def test_abs_estimated_cost(self):
        self.assertEqual(21, self._test_abs_operator.estimated_cost())

    def test_abs_get_probability_distribution(self):
        self.assertEqual(
            {1: 2, 4: 1, 5: 1},
            self._test_abs_operator.get_probability_distribution().get_result_map(),
        )
