import unittest
import unittest.mock as mock

import hypothesis
import hypothesis.strategies as strategies

from python_dice.interface.constraint.i_constraint_set import IConstraintSet
from python_dice.src.probability_distribution.probability_outcome import ProbabilityOutcome


# pylint: disable=too-many-public-methods
class TestProbabilityOutcome(unittest.TestCase):
    def setUp(self) -> None:
        self._constraint_sets = [mock.create_autospec(IConstraintSet) for _ in range(3)]
        for constraint_set in self._constraint_sets:
            constraint_set.combine_sets.return_value = self._constraint_sets[2]

        self._non_probability_outcome = {
            "str": "str",
            "int": 12,
            "float": 34.5,
            "dict": {"a": 1, "c": 3},
            "list": [1, 2, 3],
            "set": {1, 3, 4},
        }

    @hypothesis.given(strategies.integers())
    @hypothesis.settings(deadline=1000)
    def test_value(self, int_value: int):
        probability_outcome = ProbabilityOutcome(value=int_value, constraint_set=self._constraint_sets[0])
        self.assertEqual(int_value, probability_outcome.value)

    def test_type_error_on_non_int_value(self):
        for name, value in self._non_probability_outcome.items():
            if name == "int":
                continue
            with self.subTest(name):
                with self.assertRaises(TypeError):
                    _ = ProbabilityOutcome(value=value, constraint_set=self._constraint_sets[0])

    @hypothesis.given(strategies.integers(min_value=0, max_value=2))
    @hypothesis.settings(deadline=1000)
    def test_constraint_set(self, index: int):
        probability_outcome = ProbabilityOutcome(value=1, constraint_set=self._constraint_sets[index])
        self.assertEqual(self._constraint_sets[index], probability_outcome.constraint_set)

    @hypothesis.given(strategies.booleans())
    @hypothesis.settings(deadline=1000)
    def test_is_possible(self, constraint_is_possible: bool):
        self._constraint_sets[0].is_possible.return_value = constraint_is_possible
        probability_outcome = ProbabilityOutcome(value=1, constraint_set=self._constraint_sets[0])
        self.assertEqual(constraint_is_possible, probability_outcome.is_possible())

    @hypothesis.given(strategies.integers(), strategies.integers())
    @hypothesis.settings(deadline=1000)
    def test_add(self, value_one: int, value_two: int):
        probability_outcome_one = ProbabilityOutcome(value=value_one, constraint_set=self._constraint_sets[0])
        probability_outcome_two = ProbabilityOutcome(value=value_two, constraint_set=self._constraint_sets[1])

        new_probability_outcome = probability_outcome_one + probability_outcome_two
        self.assertEqual(value_one + value_two, new_probability_outcome.value)
        self.assertEqual(str(self._constraint_sets[-1]), str(new_probability_outcome.constraint_set))

    def test_add_non_probability_outcome(self):
        probability_outcome = ProbabilityOutcome(value=1, constraint_set=self._constraint_sets[1])
        for name, value in self._non_probability_outcome.items():
            with self.subTest(name):
                with self.assertRaises(TypeError):
                    _ = probability_outcome + value

    @hypothesis.given(strategies.integers(), strategies.integers())
    @hypothesis.settings(deadline=1000)
    def test_sub(self, value_one: int, value_two: int):
        probability_outcome_one = ProbabilityOutcome(value=value_one, constraint_set=self._constraint_sets[0])
        probability_outcome_two = ProbabilityOutcome(value=value_two, constraint_set=self._constraint_sets[1])

        new_probability_outcome = probability_outcome_one - probability_outcome_two
        self.assertEqual(value_one - value_two, new_probability_outcome.value)
        self.assertEqual(str(self._constraint_sets[-1]), str(new_probability_outcome.constraint_set))

    def test_sub_non_probability_outcome(self):
        probability_outcome = ProbabilityOutcome(value=1, constraint_set=self._constraint_sets[1])
        for name, value in self._non_probability_outcome.items():
            with self.subTest(name):
                with self.assertRaises(TypeError):
                    _ = probability_outcome - value

    @hypothesis.given(strategies.integers(), strategies.integers())
    @hypothesis.settings(deadline=1000)
    def test_mul(self, value_one: int, value_two: int):
        probability_outcome_one = ProbabilityOutcome(value=value_one, constraint_set=self._constraint_sets[0])
        probability_outcome_two = ProbabilityOutcome(value=value_two, constraint_set=self._constraint_sets[1])

        new_probability_outcome = probability_outcome_one * probability_outcome_two
        self.assertEqual(value_one * value_two, new_probability_outcome.value)
        self.assertEqual(str(self._constraint_sets[-1]), str(new_probability_outcome.constraint_set))

    def test_mul_non_probability_outcome(self):
        probability_outcome = ProbabilityOutcome(value=1, constraint_set=self._constraint_sets[1])
        for name, value in self._non_probability_outcome.items():
            with self.subTest(name):
                with self.assertRaises(TypeError):
                    _ = probability_outcome * value

    @hypothesis.given(strategies.integers(), strategies.integers())
    @hypothesis.settings(deadline=1000)
    def test_floordiv(self, value_one: int, value_two: int):
        hypothesis.assume(value_two != 0)
        probability_outcome_one = ProbabilityOutcome(value=value_one, constraint_set=self._constraint_sets[0])
        probability_outcome_two = ProbabilityOutcome(value=value_two, constraint_set=self._constraint_sets[1])

        new_probability_outcome = probability_outcome_one // probability_outcome_two
        self.assertEqual(value_one // value_two, new_probability_outcome.value)
        self.assertEqual(str(self._constraint_sets[-1]), str(new_probability_outcome.constraint_set))

    @hypothesis.given(strategies.integers())
    @hypothesis.settings(deadline=1000)
    def test_floordiv_div_zero(self, value_one: int):
        probability_outcome_one = ProbabilityOutcome(value=value_one, constraint_set=self._constraint_sets[0])
        probability_outcome_two = ProbabilityOutcome(value=0, constraint_set=self._constraint_sets[1])

        with self.assertRaises(ZeroDivisionError):
            _ = probability_outcome_one // probability_outcome_two

    def test_floordiv_non_probability_outcome(self):
        probability_outcome = ProbabilityOutcome(value=1, constraint_set=self._constraint_sets[1])
        for name, value in self._non_probability_outcome.items():
            with self.subTest(name):
                with self.assertRaises(TypeError):
                    _ = probability_outcome // value

    @hypothesis.given(strategies.integers(), strategies.integers())
    @hypothesis.settings(deadline=1000)
    def test_equal(self, value_one: int, value_two: int):
        probability_outcome_one = ProbabilityOutcome(value=value_one, constraint_set=self._constraint_sets[0])
        probability_outcome_two = ProbabilityOutcome(value=value_two, constraint_set=self._constraint_sets[1])

        new_probability_outcome = probability_outcome_one.__equal__(probability_outcome_two)
        self.assertEqual(1 if value_one == value_two else 0, new_probability_outcome.value)
        self.assertEqual(str(self._constraint_sets[-1]), str(new_probability_outcome.constraint_set))

    def test_equal_non_probability_outcome(self):
        probability_outcome = ProbabilityOutcome(value=1, constraint_set=self._constraint_sets[1])
        for name, value in self._non_probability_outcome.items():
            with self.subTest(name):
                with self.assertRaises(TypeError):
                    _ = probability_outcome.__equal__(value)

    @hypothesis.given(strategies.integers(), strategies.integers())
    @hypothesis.settings(deadline=1000)
    def test_not_equal(self, value_one: int, value_two: int):
        probability_outcome_one = ProbabilityOutcome(value=value_one, constraint_set=self._constraint_sets[0])
        probability_outcome_two = ProbabilityOutcome(value=value_two, constraint_set=self._constraint_sets[1])

        new_probability_outcome = probability_outcome_one.__not_equal__(probability_outcome_two)
        self.assertEqual(1 if value_one != value_two else 0, new_probability_outcome.value)
        self.assertEqual(str(self._constraint_sets[-1]), str(new_probability_outcome.constraint_set))

    def test_not_equal_non_probability_outcome(self):
        probability_outcome = ProbabilityOutcome(value=1, constraint_set=self._constraint_sets[1])
        for name, value in self._non_probability_outcome.items():
            with self.subTest(name):
                with self.assertRaises(TypeError):
                    _ = probability_outcome.__not_equal__(value)

    @hypothesis.given(strategies.integers(), strategies.integers())
    @hypothesis.settings(deadline=1000)
    def test_lt(self, value_one: int, value_two: int):
        probability_outcome_one = ProbabilityOutcome(value=value_one, constraint_set=self._constraint_sets[0])
        probability_outcome_two = ProbabilityOutcome(value=value_two, constraint_set=self._constraint_sets[1])

        new_probability_outcome = probability_outcome_one < probability_outcome_two
        self.assertEqual(1 if value_one < value_two else 0, new_probability_outcome.value)
        self.assertEqual(str(self._constraint_sets[-1]), str(new_probability_outcome.constraint_set))

    def test_lt_non_probability_outcome(self):
        probability_outcome = ProbabilityOutcome(value=1, constraint_set=self._constraint_sets[1])
        for name, value in self._non_probability_outcome.items():
            with self.subTest(name):
                with self.assertRaises(TypeError):
                    _ = probability_outcome < value

    @hypothesis.given(strategies.integers(), strategies.integers())
    @hypothesis.settings(deadline=1000)
    def test_le(self, value_one: int, value_two: int):
        probability_outcome_one = ProbabilityOutcome(value=value_one, constraint_set=self._constraint_sets[0])
        probability_outcome_two = ProbabilityOutcome(value=value_two, constraint_set=self._constraint_sets[1])

        new_probability_outcome = probability_outcome_one <= probability_outcome_two
        self.assertEqual(1 if value_one <= value_two else 0, new_probability_outcome.value)
        self.assertEqual(str(self._constraint_sets[-1]), str(new_probability_outcome.constraint_set))

    def test_le_non_probability_outcome(self):
        probability_outcome = ProbabilityOutcome(value=1, constraint_set=self._constraint_sets[1])
        for name, value in self._non_probability_outcome.items():
            with self.subTest(name):
                with self.assertRaises(TypeError):
                    _ = probability_outcome <= value

    @hypothesis.given(strategies.integers(), strategies.integers())
    @hypothesis.settings(deadline=1000)
    def test_gt(self, value_one: int, value_two: int):
        probability_outcome_one = ProbabilityOutcome(value=value_one, constraint_set=self._constraint_sets[0])
        probability_outcome_two = ProbabilityOutcome(value=value_two, constraint_set=self._constraint_sets[1])

        new_probability_outcome = probability_outcome_one > probability_outcome_two
        self.assertEqual(1 if value_one > value_two else 0, new_probability_outcome.value)
        self.assertEqual(str(self._constraint_sets[-1]), str(new_probability_outcome.constraint_set))

    def test_gt_non_probability_outcome(self):
        probability_outcome = ProbabilityOutcome(value=1, constraint_set=self._constraint_sets[1])
        for name, value in self._non_probability_outcome.items():
            with self.subTest(name):
                with self.assertRaises(TypeError):
                    _ = probability_outcome > value

    @hypothesis.given(strategies.integers(), strategies.integers())
    @hypothesis.settings(deadline=1000)
    def test_ge(self, value_one: int, value_two: int):
        probability_outcome_one = ProbabilityOutcome(value=value_one, constraint_set=self._constraint_sets[0])
        probability_outcome_two = ProbabilityOutcome(value=value_two, constraint_set=self._constraint_sets[1])

        new_probability_outcome = probability_outcome_one >= probability_outcome_two
        self.assertEqual(1 if value_one >= value_two else 0, new_probability_outcome.value)
        self.assertEqual(str(self._constraint_sets[-1]), str(new_probability_outcome.constraint_set))

    def test_ge_non_probability_outcome(self):
        probability_outcome = ProbabilityOutcome(value=1, constraint_set=self._constraint_sets[1])
        for name, value in self._non_probability_outcome.items():
            with self.subTest(name):
                with self.assertRaises(TypeError):
                    _ = probability_outcome >= value

    @hypothesis.given(strategies.integers(), strategies.integers())
    @hypothesis.settings(deadline=1000)
    def test_and(self, value_one: int, value_two: int):
        probability_outcome_one = ProbabilityOutcome(value=value_one, constraint_set=self._constraint_sets[0])
        probability_outcome_two = ProbabilityOutcome(value=value_two, constraint_set=self._constraint_sets[1])

        new_probability_outcome = probability_outcome_one.__and__(probability_outcome_two)
        self.assertEqual(1 if value_one > 0 and value_two > 0 else 0, new_probability_outcome.value)
        self.assertEqual(str(self._constraint_sets[-1]), str(new_probability_outcome.constraint_set))

    def test_and_non_probability_outcome(self):
        probability_outcome = ProbabilityOutcome(value=1, constraint_set=self._constraint_sets[1])
        for name, value in self._non_probability_outcome.items():
            with self.subTest(name):
                with self.assertRaises(TypeError):
                    _ = probability_outcome.__and__(value)

    @hypothesis.given(strategies.integers(), strategies.integers())
    @hypothesis.settings(deadline=1000)
    def test_or(self, value_one: int, value_two: int):
        probability_outcome_one = ProbabilityOutcome(value=value_one, constraint_set=self._constraint_sets[0])
        probability_outcome_two = ProbabilityOutcome(value=value_two, constraint_set=self._constraint_sets[1])

        new_probability_outcome = probability_outcome_one.__or__(probability_outcome_two)
        self.assertEqual(1 if value_one > 0 or value_two > 0 else 0, new_probability_outcome.value)
        self.assertEqual(str(self._constraint_sets[-1]), str(new_probability_outcome.constraint_set))

    def test_or_non_probability_outcome(self):
        probability_outcome = ProbabilityOutcome(value=1, constraint_set=self._constraint_sets[1])
        for name, value in self._non_probability_outcome.items():
            with self.subTest(name):
                with self.assertRaises(TypeError):
                    _ = probability_outcome.__or__(value)

    @hypothesis.given(strategies.integers())
    @hypothesis.settings(deadline=1000)
    def test_not(self, value):
        probability_outcome = ProbabilityOutcome(value=value, constraint_set=self._constraint_sets[1])
        abs_probability_outcome = probability_outcome.not_operator()
        self.assertEqual(
            0 if value > 0 else 1,
            abs_probability_outcome.value,
        )

    @hypothesis.given(strategies.integers(), strategies.integers())
    @hypothesis.settings(deadline=1000)
    def test_max_operator(self, value_one: int, value_two: int):
        probability_outcome_one = ProbabilityOutcome(value=value_one, constraint_set=self._constraint_sets[0])
        probability_outcome_two = ProbabilityOutcome(value=value_two, constraint_set=self._constraint_sets[1])

        new_probability_outcome = probability_outcome_one.max_operator(probability_outcome_two)
        self.assertEqual(max(value_one, value_two), new_probability_outcome.value)
        self.assertEqual(str(self._constraint_sets[-1]), str(new_probability_outcome.constraint_set))

    def test_max_operator_non_probability_outcome(self):
        probability_outcome = ProbabilityOutcome(value=1, constraint_set=self._constraint_sets[1])
        for name, value in self._non_probability_outcome.items():
            with self.subTest(name):
                with self.assertRaises(TypeError):
                    _ = probability_outcome.max_operator(value)

    @hypothesis.given(strategies.integers(), strategies.integers())
    @hypothesis.settings(deadline=1000)
    def test_min_operator(self, value_one: int, value_two: int):
        probability_outcome_one = ProbabilityOutcome(value=value_one, constraint_set=self._constraint_sets[0])
        probability_outcome_two = ProbabilityOutcome(value=value_two, constraint_set=self._constraint_sets[1])

        new_probability_outcome = probability_outcome_one.min_operator(probability_outcome_two)
        self.assertEqual(min(value_one, value_two), new_probability_outcome.value)
        self.assertEqual(str(self._constraint_sets[-1]), str(new_probability_outcome.constraint_set))

    def test_min_operator_non_probability_outcome(self):
        probability_outcome = ProbabilityOutcome(value=1, constraint_set=self._constraint_sets[1])
        for name, value in self._non_probability_outcome.items():
            with self.subTest(name):
                with self.assertRaises(TypeError):
                    _ = probability_outcome.min_operator(value)

    @hypothesis.given(strategies.integers())
    @hypothesis.settings(deadline=1000)
    def test_abs(self, value):
        probability_outcome = ProbabilityOutcome(value=value, constraint_set=self._constraint_sets[1])
        abs_probability_outcome = abs(probability_outcome)
        self.assertEqual(
            abs(value),
            abs_probability_outcome.value,
        )

    @hypothesis.given(strategies.integers())
    @hypothesis.settings(deadline=1000)
    def test_str(self, value):
        probability_outcome = ProbabilityOutcome(value=value, constraint_set=self._constraint_sets[1])
        self.assertEqual(
            f"ProbabilityOutcome: value={value}, constraint_set={self._constraint_sets[1]}", str(probability_outcome)
        )

    @hypothesis.given(strategies.integers())
    @hypothesis.settings(deadline=1000)
    def test_repr(self, value):
        probability_outcome = ProbabilityOutcome(value=value, constraint_set=self._constraint_sets[1])
        self.assertEqual(
            f"ProbabilityOutcome: value={value}, constraint_set={self._constraint_sets[1]}", repr(probability_outcome)
        )

    @hypothesis.given(strategies.integers())
    @hypothesis.settings(deadline=1000)
    def test_hash_the_same(self, value):
        probability_outcome_one = ProbabilityOutcome(value=value, constraint_set=self._constraint_sets[0])
        probability_outcome_two = ProbabilityOutcome(value=value, constraint_set=self._constraint_sets[0])
        self.assertEqual(hash(probability_outcome_one), hash(probability_outcome_two))

    @hypothesis.given(strategies.integers())
    @hypothesis.settings(deadline=1000)
    def test_hash_not_the_same_constraint_set(self, value):
        probability_outcome_one = ProbabilityOutcome(value=value, constraint_set=self._constraint_sets[0])
        probability_outcome_two = ProbabilityOutcome(value=value, constraint_set=self._constraint_sets[1])
        self.assertNotEqual(hash(probability_outcome_one), hash(probability_outcome_two))

    @hypothesis.given(strategies.lists(strategies.integers(), min_size=2, max_size=2, unique=True))
    @hypothesis.settings(deadline=1000)
    def test_hash_not_the_same_value(self, values):
        probability_outcome_one = ProbabilityOutcome(value=values[0], constraint_set=self._constraint_sets[0])
        probability_outcome_two = ProbabilityOutcome(value=values[1], constraint_set=self._constraint_sets[0])
        self.assertNotEqual(hash(probability_outcome_one), hash(probability_outcome_two))

    @hypothesis.given(strategies.integers())
    @hypothesis.settings(deadline=1000)
    def test_eq_true(self, value):
        probability_outcome_one = ProbabilityOutcome(value=value, constraint_set=self._constraint_sets[0])
        probability_outcome_two = ProbabilityOutcome(value=value, constraint_set=self._constraint_sets[0])
        self.assertEqual(probability_outcome_one, probability_outcome_two)

    def test_eq_true_same_object(self):
        probability_outcome = ProbabilityOutcome(value=1, constraint_set=self._constraint_sets[0])
        self.assertEqual(probability_outcome, probability_outcome)

    @hypothesis.given(strategies.lists(strategies.integers(), min_size=2, max_size=2, unique=True))
    @hypothesis.settings(deadline=1000)
    def test_eq_false_value(self, values):
        probability_outcome_one = ProbabilityOutcome(value=values[0], constraint_set=self._constraint_sets[0])
        probability_outcome_two = ProbabilityOutcome(value=values[1], constraint_set=self._constraint_sets[0])
        self.assertNotEqual(probability_outcome_one, probability_outcome_two)

    @hypothesis.given(strategies.integers())
    @hypothesis.settings(deadline=1000)
    def test_eq_false_constraint_set(self, value):
        probability_outcome_one = ProbabilityOutcome(value=value, constraint_set=self._constraint_sets[0])
        probability_outcome_two = ProbabilityOutcome(value=value, constraint_set=self._constraint_sets[1])
        self.assertNotEqual(probability_outcome_one, probability_outcome_two)

    def test_eq_error_on_non_probability_outcome(self):
        probability_outcome = ProbabilityOutcome(value=1, constraint_set=self._constraint_sets[1])
        for name, value in self._non_probability_outcome.items():
            with self.subTest(name):
                with self.assertRaises(TypeError):
                    _ = probability_outcome == value
