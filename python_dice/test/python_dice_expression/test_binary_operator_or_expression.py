import unittest
import unittest.mock as mock

import rply

import python_dice.interface.python_dice_expression.i_dice_expression as i_dice_expression
import python_dice.src.probability_distribution as probability_distribution
import python_dice.src.python_dice_expression.binary_operator_expression as binary_operator_expression


class TestBinaryOperatorOrExpression(unittest.TestCase):
    def setUp(self):
        self._mock_syntax = [
            mock.create_autospec(i_dice_expression.IDiceExpression) for _ in range(2)
        ]
        self._mock_syntax[0].roll.return_value = 10
        self._mock_syntax[0].max.return_value = 8
        self._mock_syntax[0].min.return_value = 6
        self._mock_syntax[0].__str__.return_value = "7"
        self._mock_syntax[0].estimated_cost.return_value = 9
        self._mock_syntax[
            0
        ].get_probability_distribution.return_value = probability_distribution.ProbabilityDistribution(
            {-3: 1, 0: 2, 4: 1}
        )

        self._mock_syntax[1].roll.return_value = 4
        self._mock_syntax[1].max.return_value = 6
        self._mock_syntax[1].min.return_value = 8
        self._mock_syntax[1].__str__.return_value = "2d8"
        self._mock_syntax[1].estimated_cost.return_value = 7
        self._mock_syntax[
            1
        ].get_probability_distribution.return_value = probability_distribution.ProbabilityDistribution(
            {-3: 2, 0: 1, 1: 2, 4: 1}
        )

        self._test_binary_operator = (
            binary_operator_expression.BinaryOperatorExpression(
                "OR", self._mock_syntax[0], self._mock_syntax[1]
            )
        )
        self._mock_parser_gen = mock.create_autospec(rply.ParserGenerator)

    def test_binary_operator_or_production_function(self):
        binary_operator_expression.BinaryOperatorExpression.add_production_function(
            self._mock_parser_gen
        )
        self._mock_parser_gen.production.assert_called_once_with(
            """expression : expression BINARY_OPERATOR expression"""
        )

    def test_or_roll_false(self):
        self._mock_syntax[0].roll.return_value = 0
        self._mock_syntax[1].roll.return_value = 0
        for _ in range(100):
            self.assertEqual(0, self._test_binary_operator.roll())

    def test_or_roll_true(self):
        self._mock_syntax[0].roll.return_value = 4
        for _ in range(100):
            self.assertEqual(1, self._test_binary_operator.roll())

    def test_and_max_true(self):
        self.assertEqual(1, self._test_binary_operator.max())

    def test_or_max_false(self):
        self._mock_syntax[
            0
        ].get_probability_distribution.return_value = probability_distribution.ProbabilityDistribution(
            {0: 1}
        )
        self._mock_syntax[
            1
        ].get_probability_distribution.return_value = probability_distribution.ProbabilityDistribution(
            {0: 1}
        )

        self.assertEqual(0, self._test_binary_operator.max())

    def test_or_min_true(self):
        self._mock_syntax[
            0
        ].get_probability_distribution.return_value = probability_distribution.ProbabilityDistribution(
            {4: 1}
        )
        self._mock_syntax[
            1
        ].get_probability_distribution.return_value = probability_distribution.ProbabilityDistribution(
            {4: 1}
        )
        self.assertEqual(1, self._test_binary_operator.min())

    def test_or_min_false(self):
        self.assertEqual(0, self._test_binary_operator.min())

    def test_or_str(self):
        self.assertEqual("7 OR 2d8", str(self._test_binary_operator))

    def test_or_estimated_cost(self):
        self.assertEqual(16, self._test_binary_operator.estimated_cost())

    def test_or_get_probability_distribution(self):
        self.assertEqual(
            {0: 9, 1: 15},
            self._test_binary_operator.get_probability_distribution().get_result_map(),
        )
