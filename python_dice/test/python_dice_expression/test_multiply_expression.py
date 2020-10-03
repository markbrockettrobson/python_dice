import unittest
import unittest.mock as mock

import rply

import python_dice.interface.python_dice_expression.i_dice_expression as i_dice_expression
import python_dice.src.probability_distribution as probability_distribution
import python_dice.src.python_dice_expression.multiply_expression as multiply_expression


class TestMultiplyExpression(unittest.TestCase):
    def setUp(self):
        self._mock_syntax = [
            mock.create_autospec(i_dice_expression.IDiceExpression) for _ in range(2)
        ]
        self._mock_syntax[0].roll.return_value = 10
        self._mock_syntax[0].max.return_value = 8
        self._mock_syntax[0].min.return_value = 2
        self._mock_syntax[0].__str__.return_value = "7"
        self._mock_syntax[0].estimated_cost.return_value = 9
        self._mock_syntax[
            0
        ].get_probability_distribution.return_value = probability_distribution.ProbabilityDistribution(
            {-2: 1, 4: 1}
        )

        self._mock_syntax[1].roll.return_value = 4
        self._mock_syntax[1].max.return_value = 6
        self._mock_syntax[1].min.return_value = 8
        self._mock_syntax[1].__str__.return_value = "2"
        self._mock_syntax[1].estimated_cost.return_value = 7
        self._mock_syntax[
            1
        ].get_probability_distribution.return_value = probability_distribution.ProbabilityDistribution(
            {8: 1, -3: 2}
        )

        self._test_multiply = multiply_expression.MultiplyExpression(
            self._mock_syntax[0], self._mock_syntax[1]
        )
        self._mock_parser_gen = mock.create_autospec(rply.ParserGenerator)

    def test_multiply_add_production_function(self):
        multiply_expression.MultiplyExpression.add_production_function(
            self._mock_parser_gen
        )
        self._mock_parser_gen.production.assert_called_once_with(
            """expression : expression MULTIPLY expression"""
        )

    def test_multiply_roll(self):
        for _ in range(100):
            self.assertEqual(40, self._test_multiply.roll())

    def test_multiply_max(self):
        self.assertEqual(32, self._test_multiply.max())

    def test_multiply_min(self):
        self.assertEqual(-16, self._test_multiply.min())

    def test_multiply_str(self):
        self.assertEqual("7 * 2", str(self._test_multiply))

    def test_multiply_get_probability_distribution(self):
        self._mock_syntax[
            0
        ].get_probability_distribution.return_value = probability_distribution.ProbabilityDistribution(
            {10: 1, -12: 2, 0: 1}
        )
        self._mock_syntax[
            1
        ].get_probability_distribution.return_value = probability_distribution.ProbabilityDistribution(
            {2: 1, 3: 2}
        )
        self.assertEqual(
            {-36: 4, -24: 2, 0: 3, 20: 1, 30: 2},
            self._test_multiply.get_probability_distribution().get_result_map(),
        )
