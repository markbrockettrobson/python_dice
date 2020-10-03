import unittest
import unittest.mock as mock

import rply

import python_dice.interface.i_probability_distribution as i_probability_distribution
import python_dice.interface.i_probability_state as i_probability_state
import python_dice.interface.python_dice_expression.i_dice_expression as i_dice_expression
import python_dice.src.probability_distribution as probability_distribution
import python_dice.src.python_dice_expression.var_assignment_expression as var_assignment_expression


class TestVarAssignmentExpression(unittest.TestCase):
    def setUp(self):
        self._mock_syntax = mock.create_autospec(i_dice_expression.IDiceExpression)
        self._mock_syntax.roll.return_value = 2
        self._mock_syntax.max.return_value = 8
        self._mock_syntax.min.return_value = 6
        self._mock_syntax.__str__.return_value = "7d3"
        self._mock_syntax.estimated_cost.return_value = 45
        self._mock_syntax.get_probability_distribution.return_value = probability_distribution.ProbabilityDistribution(
            {-5: 1, 1: 2, 4: 1}
        )
        self._test_name = "test_name"

        self._mock_state = mock.create_autospec(
            i_probability_state.IProbabilityDistributionState, spec_set=True
        )

        self._test_assignment_expression = var_assignment_expression.VarAssignmentExpression(
            self._mock_state, self._test_name, self._mock_syntax
        )
        self._mock_parser_gen = mock.create_autospec(rply.ParserGenerator)

    def test_var_assignment_add_production_function(self):
        var_assignment_expression.VarAssignmentExpression.add_production_function(
            self._mock_parser_gen
        )
        self._mock_parser_gen.production.assert_called_once_with(
            """expression : VAR NAME ASSIGNMENT expression"""
        )

    def test_var_assignment_roll(self):
        for _ in range(100):
            self.assertEqual(2, self._test_assignment_expression.roll())
        self._mock_state.set_constant.assert_called_with(self._test_name, 2)

    def test_var_assignment_max(self):
        self.assertEqual(8, self._test_assignment_expression.max())
        self._mock_state.set_constant.assert_called_with(self._test_name, 8)

    def test_var_assignment_min(self):
        self.assertEqual(6, self._test_assignment_expression.min())
        self._mock_state.set_constant.assert_called_with(self._test_name, 6)

    def test_var_assignment_str(self):
        self.assertEqual(
            f"VAR {self._test_name} = 7d3", str(self._test_assignment_expression)
        )

    def test_var_assignment_estimated_cost(self):
        self.assertEqual(45, self._test_assignment_expression.estimated_cost())

    def test_var_get_probability_distribution(self):
        mock_probability_distribution = mock.create_autospec(
            i_probability_distribution.IProbabilityDistribution
        )
        self._mock_syntax.get_probability_distribution.return_value = (
            mock_probability_distribution
        )
        self.assertEqual(
            mock_probability_distribution,
            self._test_assignment_expression.get_probability_distribution(),
        )
        self._mock_state.set_var.assert_called_with(
            self._test_name, mock_probability_distribution
        )
