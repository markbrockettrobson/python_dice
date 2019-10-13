import unittest
import unittest.mock as mock

import rply

import python_dice.interface.python_dice_expression.i_dice_expression as i_dice_expression
import python_dice.src.probability_distribution as probability_distribution
import python_dice.src.python_dice_expression.integer_division_expression as integer_division_expression


class TestIntegerDivisionExpression(unittest.TestCase):
    def setUp(self):
        self._mock_syntax = [
            mock.create_autospec(i_dice_expression.IDiceExpression) for _ in range(4)
        ]
        self._mock_syntax[0].roll.return_value = 10
        self._mock_syntax[0].max.return_value = 8
        self._mock_syntax[0].min.return_value = 201
        self._mock_syntax[0].__str__.return_value = "7"
        self._mock_syntax[
            0
        ].get_probability_distribution.return_value = probability_distribution.ProbabilityDistribution(
            {201: 1, -10: 1}
        )

        self._mock_syntax[1].roll.return_value = 3
        self._mock_syntax[1].max.return_value = 8
        self._mock_syntax[1].min.return_value = 2
        self._mock_syntax[1].__str__.return_value = "2"
        self._mock_syntax[
            1
        ].get_probability_distribution.return_value = probability_distribution.ProbabilityDistribution(
            {2: 1, -2: 1}
        )
        self._mock_syntax[
            2
        ].get_probability_distribution.return_value = probability_distribution.ProbabilityDistribution(
            {10: 1, 12: 2}
        )
        self._mock_syntax[
            3
        ].get_probability_distribution.return_value = probability_distribution.ProbabilityDistribution(
            {2: 1, 3: 2, 0: 10}
        )
        self._test_integer_division = integer_division_expression.IntegerDivisionExpression(
            self._mock_syntax[0], self._mock_syntax[1]
        )
        self._mock_parser_gen = mock.create_autospec(rply.ParserGenerator)

    def test_integer_division_add_production_function(self):
        integer_division_expression.IntegerDivisionExpression.add_production_function(
            self._mock_parser_gen
        )
        self._mock_parser_gen.production.assert_called_once_with(
            """expression : expression INTEGER_DIVISION expression"""
        )

    def test_integer_division_roll(self):
        for _ in range(100):
            self.assertEqual(3, self._test_integer_division.roll())

    def test_integer_division_roll_raise_on_zero(self):
        self._mock_syntax[1].roll.return_value = 0
        self.assertRaises(ZeroDivisionError, self._test_integer_division.roll)

    def test_integer_division_max(self):
        self.assertEqual(100, self._test_integer_division.max())

    def test_integer_division_max_raise_on_zero(self):
        self._test_integer_division = integer_division_expression.IntegerDivisionExpression(
            self._mock_syntax[2], self._mock_syntax[3]
        )
        self.assertRaises(ZeroDivisionError, self._test_integer_division.max)

    def test_integer_division_min(self):
        self.assertEqual(-101, self._test_integer_division.min())

    def test_integer_division_min_raise_on_zero(self):
        self._test_integer_division = integer_division_expression.IntegerDivisionExpression(
            self._mock_syntax[2], self._mock_syntax[3]
        )
        self.assertRaises(ZeroDivisionError, self._test_integer_division.min)

    def test_integer_division_str(self):
        self.assertEqual("7 // 2", str(self._test_integer_division))

    def test_integer_division_get_probability_distribution(self):
        self._mock_syntax[
            0
        ].get_probability_distribution.return_value = probability_distribution.ProbabilityDistribution(
            {10: 1, 12: 2, 0: 1}
        )
        self._mock_syntax[
            1
        ].get_probability_distribution.return_value = probability_distribution.ProbabilityDistribution(
            {2: 1, 3: 2}
        )
        self.assertEqual(
            {5: 1, 6: 2, 3: 2, 4: 4, 0: 3},
            self._test_integer_division.get_probability_distribution().get_result_map(),
        )

    def test_integer_division_get_probability_distribution_raise_on_zero(self):
        self._test_integer_division = integer_division_expression.IntegerDivisionExpression(
            self._mock_syntax[2], self._mock_syntax[3]
        )
        self.assertRaises(
            ZeroDivisionError, self._test_integer_division.get_probability_distribution
        )
