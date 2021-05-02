from unittest import TestCase
from unittest.mock import create_autospec

import rply  # type: ignore

from python_dice.interface.expression.i_dice_expression import IDiceExpression
from python_dice.src.expression.not_expression import NotExpression
from python_dice.src.probability_distribution.probability_distribution_factory import ProbabilityDistributionFactory


class TestBinaryOperatorNotExpression(TestCase):
    def setUp(self):
        self._probability_distribution_factory = ProbabilityDistributionFactory()

        self._mock_syntax = create_autospec(IDiceExpression)
        self._mock_syntax.roll.return_value = 0
        self._mock_syntax.max.return_value = 8
        self._mock_syntax.min.return_value = 6
        self._mock_syntax.__str__.return_value = "7d3"
        self._mock_syntax.estimated_cost.return_value = 9
        self._mock_syntax.get_probability_distribution.return_value = self._probability_distribution_factory.create(
            {-3: 1, 0: 2, 4: 1}
        )
        self._mock_syntax.get_contained_variables.return_value = {"mock"}

        self._test_binary_operator = NotExpression(self._mock_syntax)
        self._mock_parser_gen = create_autospec(rply.ParserGenerator)

    def test_binary_operator_add_production_function(self):
        NotExpression.add_production_function(self._mock_parser_gen, self._probability_distribution_factory)
        self._mock_parser_gen.production.assert_called_once_with("""expression : NOT expression""")

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
        self._mock_syntax.get_probability_distribution.return_value = self._probability_distribution_factory.create(
            {4: 1, 54: 1}
        )
        self.assertEqual(0, self._test_binary_operator.max())

    def test_ne_min_true(self):
        self._mock_syntax.get_probability_distribution.return_value = self._probability_distribution_factory.create(
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
            {0: 1, 1: 3},
            self._test_binary_operator.get_probability_distribution().get_result_map(),
        )

    def test_ne_get_contained_variables(self):
        self.assertSetEqual(
            {"mock"},
            self._test_binary_operator.get_contained_variables(),
        )
