import unittest

from python_dice.src.constraint.constraint_factory import ConstraintFactory
from python_dice.src.probability_distribution.probability_distribution_factory import ProbabilityDistributionFactory
from python_dice.src.probability_distribution.probability_distribution_state import ProbabilityDistributionState
from python_dice.src.probability_distribution.probability_outcome_factory import ProbabilityOutcomeFactory


class TestProbabilityState(unittest.TestCase):
    def setUp(self) -> None:
        self._probability_distribution_factory = ProbabilityDistributionFactory()
        self._probability_outcome_factory = ProbabilityOutcomeFactory()
        self._constraint_factory = ConstraintFactory()

        self._test_name = "test_name"

        _1_n5 = self._probability_outcome_factory.create_empty(-5)
        _1_n5.constraint_set.add_constraint(self._constraint_factory.var_value_constraint("test_name_1", {-5}))
        _1_1 = self._probability_outcome_factory.create_empty(1)
        _1_1.constraint_set.add_constraint(self._constraint_factory.var_value_constraint("test_name_1", {1}))

        _1_4 = self._probability_outcome_factory.create_empty(4)
        _1_4.constraint_set.add_constraint(self._constraint_factory.var_value_constraint("test_name_1", {4}))

        _2_n5 = self._probability_outcome_factory.create_empty(-5)
        _2_n5.constraint_set.add_constraint(self._constraint_factory.var_value_constraint("test_name_2", {-5}))
        _2_1 = self._probability_outcome_factory.create_empty(1)
        _2_1.constraint_set.add_constraint(self._constraint_factory.var_value_constraint("test_name_2", {1}))

        _2_4 = self._probability_outcome_factory.create_empty(4)
        _2_4.constraint_set.add_constraint(self._constraint_factory.var_value_constraint("test_name_2", {4}))

        self._test_distribution = self._probability_distribution_factory.create({-5: 1, 1: 2, 4: 1})
        self._return_one_distribution = self._probability_distribution_factory.create({_1_n5: 1, _1_1: 2, _1_4: 1})
        self._return_two_distribution = self._probability_distribution_factory.create({_2_n5: 1, _2_1: 2, _2_4: 1})

        self._test_int = 1
        self._test_probability_state = ProbabilityDistributionState(
            self._probability_distribution_factory, self._constraint_factory
        )

    def test_probability_state_has_constant_false(self):
        self._test_probability_state.set_constant("a", self._test_int)
        self.assertFalse(self._test_probability_state.has_constant(self._test_name))

    def test_probability_state_has_constant_true(self):
        self._test_probability_state.set_constant(self._test_name, self._test_int)
        self.assertTrue(self._test_probability_state.has_constant(self._test_name))

    def test_probability_state_has_var_false(self):
        self._test_probability_state.set_var("a", self._test_distribution)
        self.assertFalse(self._test_probability_state.has_var(self._test_name))

    def test_probability_state_has_var_true(self):
        self._test_probability_state.set_var(self._test_name, self._test_distribution)
        self.assertTrue(self._test_probability_state.has_var(self._test_name))

    def test_probability_state_get_constant_false(self):
        self._test_probability_state.set_constant("a", self._test_int)
        with self.assertRaises(KeyError):
            self._test_probability_state.get_constant(self._test_name)

    def test_probability_state_get_constant_true(self):
        self._test_probability_state.set_constant(self._test_name, self._test_int)
        self.assertEqual(self._test_int, self._test_probability_state.get_constant(self._test_name))

    def test_probability_state_get_var_false(self):
        self._test_probability_state.set_var("a", self._test_distribution)
        with self.assertRaises(KeyError):
            self._test_probability_state.get_var(self._test_name)

    def test_probability_state_get_var_dict(self):
        self._test_probability_state.set_var(self._test_name, self._test_distribution)

        self.assertIn(
            self._test_name,
            self._test_probability_state.get_var_dict(),
        )
        self.assertEqual(
            str(self._return_one_distribution), str(self._test_probability_state.get_var_dict()[self._test_name])
        )

    def test_probability_state_get_var_dict_second_time(self):
        self._test_probability_state.set_var(self._test_name, self._test_distribution)
        self._test_probability_state.set_var(self._test_name, self._test_distribution)

        self.assertIn(
            self._test_name,
            self._test_probability_state.get_var_dict(),
        )

        self.assertEqual(
            str(self._return_two_distribution), str(self._test_probability_state.get_var_dict()[self._test_name])
        )

    def test_probability_state_get_constant_dict(self):
        self._test_probability_state.set_constant(self._test_name, self._test_int)
        self.assertEqual(
            {self._test_name: self._test_int},
            self._test_probability_state.get_constant_dict(),
        )
