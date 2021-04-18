import unittest
import unittest.mock as mock

import rply  # type: ignore

from python_dice.interface.expression.i_dice_expression import IDiceExpression
from python_dice.src.expression.minmax_expression import MinMaxExpression
from python_dice.src.probability_distribution.probability_distribution import ProbabilityDistribution


class TestAddExpression(unittest.TestCase):
    def setUp(self):
        self._mock_syntax = [mock.create_autospec(IDiceExpression) for _ in range(2)]
        self._mock_syntax[0].roll.return_value = 10
        self._mock_syntax[0].max.return_value = 8
        self._mock_syntax[0].min.return_value = 6
        self._mock_syntax[0].__str__.return_value = "7d7"
        self._mock_syntax[0].estimated_cost.return_value = 9
        self._mock_syntax[0].get_probability_distribution.return_value = ProbabilityDistribution({-2: 1, 4: 1})
        self._mock_syntax[0].get_contained_variables.return_value = {"mock one"}

        self._mock_syntax[1].roll.return_value = 4
        self._mock_syntax[1].max.return_value = 6
        self._mock_syntax[1].min.return_value = 8
        self._mock_syntax[1].__str__.return_value = "2d2"
        self._mock_syntax[1].estimated_cost.return_value = 7
        self._mock_syntax[1].get_probability_distribution.return_value = ProbabilityDistribution({8: 1, -3: 2})
        self._mock_syntax[1].get_contained_variables.return_value = {"mock two"}

        self._test_minmax = MinMaxExpression("MAX", self._mock_syntax[0], self._mock_syntax[1])
        self._mock_parser_gen = mock.create_autospec(rply.ParserGenerator)

    def test_minmax_add_production_function(self):
        MinMaxExpression.add_production_function(self._mock_parser_gen)
        self._mock_parser_gen.production.assert_called_once_with(
            """expression : MINMAX OPEN_PARENTHESIS expression COMMA expression CLOSE_PARENTHESIS"""
        )

    def test_max_roll(self):
        for _ in range(100):
            self.assertEqual(10, self._test_minmax.roll())

    def test_min_roll(self):
        self._test_minmax = MinMaxExpression("MIN", self._mock_syntax[0], self._mock_syntax[1])
        for _ in range(100):
            self.assertEqual(4, self._test_minmax.roll())

    def test_max_max(self):
        self.assertEqual(8, self._test_minmax.max())

    def test_min_max(self):
        self._test_minmax = MinMaxExpression("MIN", self._mock_syntax[0], self._mock_syntax[1])
        self.assertEqual(6, self._test_minmax.max())

    def test_max_min(self):
        self.assertEqual(8, self._test_minmax.max())

    def test_min_min(self):
        self._test_minmax = MinMaxExpression("MIN", self._mock_syntax[0], self._mock_syntax[1])
        self.assertEqual(6, self._test_minmax.min())

    def test_max_str(self):
        self.assertEqual("MAX(7d7, 2d2)", str(self._test_minmax))

    def test_min_str(self):
        self._test_minmax = MinMaxExpression("MIN", self._mock_syntax[0], self._mock_syntax[1])
        self.assertEqual("MIN(7d7, 2d2)", str(self._test_minmax))

    def test_min_max_estimated_cost(self):
        self.assertEqual(16, self._test_minmax.estimated_cost())

    def test_max_get_probability_distribution(self):
        self._mock_syntax[0].get_probability_distribution.return_value = ProbabilityDistribution({10: 1, -12: 2, 0: 1})
        self._mock_syntax[1].get_probability_distribution.return_value = ProbabilityDistribution({2: 1, 3: 2})
        self.assertEqual(
            {2: 3, 3: 6, 10: 3},
            self._test_minmax.get_probability_distribution().get_result_map(),
        )

    def test_min_get_probability_distribution(self):
        self._test_minmax = MinMaxExpression("MIN", self._mock_syntax[0], self._mock_syntax[1])
        self._mock_syntax[0].get_probability_distribution.return_value = ProbabilityDistribution({10: 1, -12: 2, 0: 1})
        self._mock_syntax[1].get_probability_distribution.return_value = ProbabilityDistribution({2: 1, 3: 2})
        self.assertEqual(
            {-12: 6, 0: 3, 2: 1, 3: 2},
            self._test_minmax.get_probability_distribution().get_result_map(),
        )

    def test_max_get_probability_distribution_second_example(self):
        self._mock_syntax[0].get_probability_distribution.return_value = ProbabilityDistribution(
            {-3: 1, -2: 1, -1: 1, 0: 1, 5: 1, 6: 1}
        )
        self._mock_syntax[1].get_probability_distribution.return_value = ProbabilityDistribution({0: 1})
        self.assertEqual(
            {0: 4, 5: 1, 6: 1},
            self._test_minmax.get_probability_distribution().get_result_map(),
        )

    def test_min_get_probability_distribution_second_example(self):
        self._test_minmax = MinMaxExpression("MIN", self._mock_syntax[0], self._mock_syntax[1])
        self._mock_syntax[0].get_probability_distribution.return_value = ProbabilityDistribution({-1: 1, 1: 1})
        self._mock_syntax[1].get_probability_distribution.return_value = ProbabilityDistribution({0: 1})
        self.assertEqual(
            {0: 1, -1: 1},
            self._test_minmax.get_probability_distribution().get_result_map(),
        )

    def test_max_get_probability_distribution_third_example(self):
        self._mock_syntax[0].get_probability_distribution.return_value = ProbabilityDistribution({-1: 1, 1: 1})
        self._mock_syntax[1].get_probability_distribution.return_value = ProbabilityDistribution({0: 1})
        self.assertEqual(
            {0: 1, 1: 1},
            self._test_minmax.get_probability_distribution().get_result_map(),
        )

    def test_min_get_probability_distribution_third_example(self):
        self._test_minmax = MinMaxExpression("MIN", self._mock_syntax[0], self._mock_syntax[1])
        self._mock_syntax[0].get_probability_distribution.return_value = ProbabilityDistribution(
            {-3: 1, -2: 1, -1: 1, 0: 1, 5: 1, 6: 1}
        )
        self._mock_syntax[1].get_probability_distribution.return_value = ProbabilityDistribution({0: 1})
        self.assertEqual(
            {-3: 1, -2: 1, -1: 1, 0: 3},
            self._test_minmax.get_probability_distribution().get_result_map(),
        )

    def test_min_get_contained_variables(self):
        self.assertSetEqual({"mock one", "mock two"}, self._test_minmax.get_contained_variables())
