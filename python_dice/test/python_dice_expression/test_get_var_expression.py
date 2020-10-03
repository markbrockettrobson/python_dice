import unittest
import unittest.mock as mock

import rply

import python_dice.interface.i_probability_state as i_probability_state
import python_dice.src.probability_distribution as probability_distribution
import python_dice.src.python_dice_expression.get_var_expression as get_var_expression


class TestGetVarExpression(unittest.TestCase):
    def setUp(self):
        self._probability_distribution = (
            probability_distribution.ProbabilityDistribution({-5: 1, 1: 2, 4: 1})
        )
        self._test_name = "test_name"

        self._mock_state = mock.create_autospec(
            i_probability_state.IProbabilityDistributionState, spec_set=True
        )
        self._mock_state.get_constant.return_value = 2
        self._mock_state.get_var.return_value = self._probability_distribution

        self._test_assignment_expression = get_var_expression.GetVarExpression(
            self._mock_state, self._test_name
        )
        self._mock_parser_gen = mock.create_autospec(rply.ParserGenerator)

    def test_get_var_add_production_function(self):
        get_var_expression.GetVarExpression.add_production_function(
            self._mock_parser_gen
        )
        self._mock_parser_gen.production.assert_called_once_with(
            """expression : NAME"""
        )

    def test_get_var_roll(self):
        for _ in range(100):
            self.assertEqual(2, self._test_assignment_expression.roll())
        self._mock_state.get_constant.assert_called_with(self._test_name)

    def test_get_var_max(self):
        self.assertEqual(2, self._test_assignment_expression.max())
        self._mock_state.get_constant.assert_called_with(self._test_name)

    def test_get_var_min(self):
        self.assertEqual(2, self._test_assignment_expression.min())
        self._mock_state.get_constant.assert_called_with(self._test_name)

    def test_var_assignment_str(self):
        self.assertEqual(f"{self._test_name}", str(self._test_assignment_expression))

    def test_var_estimated_cost(self):
        self.assertEqual(2, self._test_assignment_expression.estimated_cost())

    def test_var_get_probability_distribution(self):
        self.assertEqual(
            self._probability_distribution,
            self._test_assignment_expression.get_probability_distribution(),
        )
        self._mock_state.get_var.assert_called_with(self._test_name)
