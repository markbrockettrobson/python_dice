import unittest
import unittest.mock as mock

import rply

import python_dice.interface.python_dice_expression.i_dice_expression as i_dice_expression
import python_dice.src.probability_distribution as probability_distribution
import python_dice.src.python_dice_expression.parentheses_enclosed_expression as parentheses_enclosed_expression


class TestParenthesisEnclosedExpression(unittest.TestCase):
    def setUp(self):
        self._mock_syntax = mock.create_autospec(i_dice_expression.IDiceExpression)
        self._mock_syntax.roll.return_value = 10
        self._mock_syntax.max.return_value = 8
        self._mock_syntax.min.return_value = 6
        self._mock_syntax.__str__.return_value = "7d4"
        self._mock_syntax.estimated_cost.return_value = 987654321
        self._mock_syntax.get_probability_distribution.return_value = probability_distribution.ProbabilityDistribution(
            {-2: 1, 4: 1}
        )

        self._test_parentheses_enclosed_expression = parentheses_enclosed_expression.ParenthesisEnclosedExpression(
            self._mock_syntax
        )
        self._mock_parser_gen = mock.create_autospec(rply.ParserGenerator)

    def test_add_add_production_function(self):
        parentheses_enclosed_expression.ParenthesisEnclosedExpression.add_production_function(
            self._mock_parser_gen
        )
        self._mock_parser_gen.production.assert_called_once_with(
            """expression : OPEN_PARENTHESIS expression CLOSE_PARENTHESIS"""
        )

    def test_parenthesis_roll(self):
        for _ in range(100):
            self.assertEqual(10, self._test_parentheses_enclosed_expression.roll())

    def test_parenthesis_max(self):
        self.assertEqual(8, self._test_parentheses_enclosed_expression.max())

    def test_parenthesis_min(self):
        self.assertEqual(6, self._test_parentheses_enclosed_expression.min())

    def test_parenthesis_str(self):
        self.assertEqual("(7d4)", str(self._test_parentheses_enclosed_expression))

    def test_parenthesis_estimated_cost(self):
        self.assertEqual(
            987654321, self._test_parentheses_enclosed_expression.estimated_cost()
        )

    def test_parenthesis_get_probability_distribution(self):
        self.assertEqual(
            {-2: 1, 4: 1},
            self._test_parentheses_enclosed_expression.get_probability_distribution().get_result_map(),
        )
