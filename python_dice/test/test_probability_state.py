import unittest
import unittest.mock as mock

import python_dice.src.probability_distribution as probability_distribution
import python_dice.src.probability_state as probability_state


class TestProbabilityState(unittest.TestCase):
    def setUp(self) -> None:
        self._mock_distribution = mock.create_autospec(
            probability_distribution.ProbabilityDistribution
        )
        self._test_int = 1
        self._test_probability_state = probability_state.ProbabilityState()
        self._test_name = "test_name"

    def test_probability_state_has_constant_false(self):
        self._test_probability_state.set_constant("a", self._test_int)
        self.assertFalse(self._test_probability_state.has_constant(self._test_name))

    def test_probability_state_has_constant_true(self):
        self._test_probability_state.set_constant(self._test_name, self._test_int)
        self.assertTrue(self._test_probability_state.has_constant(self._test_name))

    def test_probability_state_has_var_false(self):
        self._test_probability_state.set_var("a", self._mock_distribution)
        self.assertFalse(self._test_probability_state.has_var(self._test_name))

    def test_probability_state_has_var_true(self):
        self._test_probability_state.set_var(self._test_name, self._mock_distribution)
        self.assertTrue(self._test_probability_state.has_var(self._test_name))

    def test_probability_state_get_constant_false(self):
        self._test_probability_state.set_constant("a", self._test_int)
        with self.assertRaises(KeyError):
            self._test_probability_state.get_constant(self._test_name)

    def test_probability_state_get_constant_true(self):
        self._test_probability_state.set_constant(self._test_name, self._test_int)
        self.assertEqual(
            self._test_int, self._test_probability_state.get_constant(self._test_name)
        )

    def test_probability_state_get_var_false(self):
        self._test_probability_state.set_var("a", self._mock_distribution)
        with self.assertRaises(KeyError):
            self._test_probability_state.get_var(self._test_name)

    def test_probability_state_get_var_true(self):
        self._test_probability_state.set_var(self._test_name, self._mock_distribution)
        self.assertEqual(
            self._mock_distribution,
            self._test_probability_state.get_var(self._test_name),
        )

    def test_probability_state_get_var_dict(self):
        self._test_probability_state.set_var(self._test_name, self._mock_distribution)
        self.assertEqual(
            {self._test_name: self._mock_distribution},
            self._test_probability_state.get_var_dict(),
        )

    def test_probability_state_get_constant_dict(self):
        self._test_probability_state.set_constant(self._test_name, self._test_int)
        self.assertEqual(
            {self._test_name: self._test_int},
            self._test_probability_state.get_constant_dict(),
        )