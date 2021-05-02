import unittest
import unittest.mock as mock

import rply  # type: ignore

from python_dice.interface.expression.i_dice_expression import IDiceExpression
from python_dice.src.expression.subtract_expression import SubtractExpression
from python_dice.src.probability_distribution.probability_distribution_factory import ProbabilityDistributionFactory


class TestSubtractExpression(unittest.TestCase):
    def setUp(self):
        self._probability_distribution_factory = ProbabilityDistributionFactory()

        self._mock_syntax = [mock.create_autospec(IDiceExpression) for _ in range(2)]
        self._mock_syntax[0].roll.return_value = 10
        self._mock_syntax[0].max.return_value = 8
        self._mock_syntax[0].min.return_value = 6
        self._mock_syntax[0].__str__.return_value = "7"
        self._mock_syntax[0].estimated_cost.return_value = 9
        self._mock_syntax[0].get_probability_distribution.return_value = self._probability_distribution_factory.create(
            {-2: 1, 4: 1}
        )
        self._mock_syntax[0].get_contained_variables.return_value = {"mock one"}

        self._mock_syntax[1].roll.return_value = 4
        self._mock_syntax[1].max.return_value = 6
        self._mock_syntax[1].min.return_value = 8
        self._mock_syntax[1].__str__.return_value = "2"
        self._mock_syntax[1].estimated_cost.return_value = 7
        self._mock_syntax[1].get_probability_distribution.return_value = self._probability_distribution_factory.create(
            {8: 1, -3: 2}
        )
        self._mock_syntax[1].get_contained_variables.return_value = {"mock two"}

        self._test_subtract = SubtractExpression(self._mock_syntax[0], self._mock_syntax[1])
        self._mock_parser_gen = mock.create_autospec(rply.ParserGenerator)

    def test_subtract_add_production_function(self):
        SubtractExpression.add_production_function(self._mock_parser_gen, self._probability_distribution_factory)
        self._mock_parser_gen.production.assert_called_once_with("""expression : expression SUBTRACT expression""")

    def test_subtract_roll(self):
        for _ in range(100):
            self.assertEqual(6, self._test_subtract.roll())

    def test_subtract_max(self):
        self.assertEqual(7, self._test_subtract.max())

    def test_subtract_min(self):
        self.assertEqual(-10, self._test_subtract.min())

    def test_subtract_str(self):
        self.assertEqual("7 - 2", str(self._test_subtract))

    def test_subtract_estimated_cost(self):
        self.assertEqual(16, self._test_subtract.estimated_cost())

    def test_subtract_get_probability_distribution(self):
        self._mock_syntax[0].get_probability_distribution.return_value = self._probability_distribution_factory.create(
            {10: 1, -12: 2, 0: 1}
        )
        self._mock_syntax[1].get_probability_distribution.return_value = self._probability_distribution_factory.create(
            {2: 1, 3: 2}
        )
        self.assertEqual(
            {8: 1, -14: 2, -2: 1, 7: 2, -15: 4, -3: 2},
            self._test_subtract.get_probability_distribution().get_result_map(),
        )

    def test_subtract_get_contained_variables(self):
        self.assertSetEqual({"mock one", "mock two"}, self._test_subtract.get_contained_variables())
