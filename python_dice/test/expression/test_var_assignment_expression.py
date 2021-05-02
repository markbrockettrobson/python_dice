import unittest
import unittest.mock as mock

import rply  # type: ignore

from python_dice.interface.expression.i_dice_expression import IDiceExpression
from python_dice.interface.probability_distribution.i_probability_distribution import IProbabilityDistribution
from python_dice.interface.probability_distribution.i_probability_distribution_state import (
    IProbabilityDistributionState,
)
from python_dice.src.expression.var_assignment_expression import VarAssignmentExpression
from python_dice.src.probability_distribution.probability_distribution_factory import ProbabilityDistributionFactory


class TestVarAssignmentExpression(unittest.TestCase):
    def setUp(self):
        self._probability_distribution_factory = ProbabilityDistributionFactory()

        self._mock_syntax = mock.create_autospec(IDiceExpression)
        self._mock_syntax.roll.return_value = 2
        self._mock_syntax.max.return_value = 8
        self._mock_syntax.min.return_value = 6
        self._mock_syntax.__str__.return_value = "7d3"
        self._mock_syntax.estimated_cost.return_value = 45
        self._mock_syntax.get_probability_distribution.return_value = self._probability_distribution_factory.create(
            {-5: 1, 1: 2, 4: 1}
        )
        self._mock_syntax.get_contained_variables.return_value = {"mock"}
        self._test_name = "test_name"

        self._mock_state = mock.create_autospec(IProbabilityDistributionState, spec_set=True)

        self._test_assignment_expression = VarAssignmentExpression(self._mock_state, self._test_name, self._mock_syntax)
        self._mock_parser_gen = mock.create_autospec(rply.ParserGenerator)

    def test_var_assignment_add_production_function(self):
        VarAssignmentExpression.add_production_function(self._mock_parser_gen, self._probability_distribution_factory)
        self._mock_parser_gen.production.assert_called_once_with("""expression : VAR NAME ASSIGNMENT expression""")

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
        self.assertEqual(f"VAR {self._test_name} = 7d3", str(self._test_assignment_expression))

    def test_var_assignment_estimated_cost(self):
        self.assertEqual(45 + 2, self._test_assignment_expression.estimated_cost())

    def test_var_get_probability_distribution(self):
        mock_probability_distribution = mock.create_autospec(IProbabilityDistribution)
        self._mock_syntax.get_probability_distribution.return_value = mock_probability_distribution
        self.assertEqual(
            mock_probability_distribution,
            self._test_assignment_expression.get_probability_distribution(),
        )
        self._mock_state.set_var.assert_called_with(self._test_name, mock_probability_distribution)

    def test_get_contained_variables(self):
        self.assertEqual(set(), self._test_assignment_expression.get_contained_variables())
