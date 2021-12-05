from unittest import TestCase

from hypothesis import given, settings
from hypothesis.strategies import integers

from python_dice.src.constraint.constraint_factory import ConstraintFactory
from python_dice.src.constraint.constraint_merger import ConstraintMerger
from python_dice.src.constraint.constraint_set import ConstraintSet
from python_dice.src.probability_distribution.probability_outcome import ProbabilityOutcome


# pylint: disable=too-many-public-methods
class TestProbabilityOutcomeIntegration(TestCase):
    TEST_DEADLINE = 2000

    def setUp(self) -> None:
        self._constraint_merger = ConstraintMerger()
        self._constraint_factory = ConstraintFactory()
        self._constraints = [
            self._constraint_factory.var_value_constraint(name="a", values={1, 2, 3, 4, 5}),
            self._constraint_factory.var_value_constraint(name="a", values={1, 2, 3, 4}),
            self._constraint_factory.var_value_constraint(name="a", values={1, 2, 3}),
            self._constraint_factory.var_value_constraint(name="a", values={1, 2}),
            self._constraint_factory.var_value_constraint(name="a", values={1}),
            self._constraint_factory.null_constraint,
            self._constraint_factory.impossible_constraint,
        ]

        self._constraint_sets = [
            ConstraintSet({self._constraints[i] for i in [1, 5]}, self._constraint_merger),
            ConstraintSet({self._constraints[i] for i in [0, 3]}, self._constraint_merger),
            ConstraintSet({self._constraints[i] for i in [3]}, self._constraint_merger),
        ]

        self._non_probability_outcome = {
            "str": "str",
            "int": 12,
            "float": 34.5,
            "dict": {"a": 1, "c": 3},
            "list": [1, 2, 3],
            "set": {1, 3, 4},
        }

    @given(integers())
    @settings(deadline=TEST_DEADLINE)
    def test_value(self, int_value: int):
        probability_outcome = ProbabilityOutcome(value=int_value, constraint_set=self._constraint_sets[0])
        self.assertEqual(int_value, probability_outcome.value)

    @given(integers(min_value=0, max_value=2))
    @settings(deadline=TEST_DEADLINE)
    def test_constraint_set(self, index: int):
        probability_outcome = ProbabilityOutcome(value=1, constraint_set=self._constraint_sets[index])
        self.assertEqual(self._constraint_sets[index], probability_outcome.constraint_set)

    def test_add(self):
        probability_outcome_one = ProbabilityOutcome(value=1234567890, constraint_set=self._constraint_sets[0])
        probability_outcome_two = ProbabilityOutcome(value=987654321, constraint_set=self._constraint_sets[1])

        new_probability_outcome = probability_outcome_one + probability_outcome_two
        self.assertEqual(1234567890 + 987654321, new_probability_outcome.value)
        self.assertEqual(str(self._constraint_sets[-1]), str(new_probability_outcome.constraint_set))

    def test_add_non_probability_outcome(self):
        probability_outcome = ProbabilityOutcome(value=1234567890, constraint_set=self._constraint_sets[1])
        for name, value in self._non_probability_outcome.items():
            with self.subTest(name):
                with self.assertRaises(TypeError):
                    _ = probability_outcome + value

    def test_sub(self):
        probability_outcome_one = ProbabilityOutcome(value=1234567890, constraint_set=self._constraint_sets[0])
        probability_outcome_two = ProbabilityOutcome(value=987654321, constraint_set=self._constraint_sets[1])

        new_probability_outcome = probability_outcome_one - probability_outcome_two
        self.assertEqual(1234567890 - 987654321, new_probability_outcome.value)
        self.assertEqual(str(self._constraint_sets[-1]), str(new_probability_outcome.constraint_set))

    def test_sub_non_probability_outcome(self):
        probability_outcome = ProbabilityOutcome(value=1234567890, constraint_set=self._constraint_sets[1])
        for name, value in self._non_probability_outcome.items():
            with self.subTest(name):
                with self.assertRaises(TypeError):
                    _ = probability_outcome - value

    def test_mul(self):
        probability_outcome_one = ProbabilityOutcome(value=1234567890, constraint_set=self._constraint_sets[0])
        probability_outcome_two = ProbabilityOutcome(value=987654321, constraint_set=self._constraint_sets[1])

        new_probability_outcome = probability_outcome_one * probability_outcome_two
        self.assertEqual(1234567890 * 987654321, new_probability_outcome.value)
        self.assertEqual(str(self._constraint_sets[-1]), str(new_probability_outcome.constraint_set))

    def test_mul_non_probability_outcome(self):
        probability_outcome = ProbabilityOutcome(value=1234567890, constraint_set=self._constraint_sets[1])
        for name, value in self._non_probability_outcome.items():
            with self.subTest(name):
                with self.assertRaises(TypeError):
                    _ = probability_outcome * value

    def test_floordiv(self):
        probability_outcome_one = ProbabilityOutcome(value=1234567890, constraint_set=self._constraint_sets[0])
        probability_outcome_two = ProbabilityOutcome(value=987654321, constraint_set=self._constraint_sets[1])

        new_probability_outcome = probability_outcome_one // probability_outcome_two
        self.assertEqual(1234567890 // 987654321, new_probability_outcome.value)
        self.assertEqual(str(self._constraint_sets[-1]), str(new_probability_outcome.constraint_set))

    def test_floordiv_non_probability_outcome(self):
        probability_outcome = ProbabilityOutcome(value=1234567890, constraint_set=self._constraint_sets[1])
        for name, value in self._non_probability_outcome.items():
            with self.subTest(name):
                with self.assertRaises(TypeError):
                    _ = probability_outcome // value

    def test_equal(self):
        probability_outcome_one = ProbabilityOutcome(value=1234567890, constraint_set=self._constraint_sets[0])
        probability_outcome_two = ProbabilityOutcome(value=987654321, constraint_set=self._constraint_sets[1])

        new_probability_outcome = probability_outcome_one.__equal__(probability_outcome_two)
        self.assertEqual(0, new_probability_outcome.value)
        self.assertEqual(str(self._constraint_sets[-1]), str(new_probability_outcome.constraint_set))

    def test_equal_non_probability_outcome(self):
        probability_outcome = ProbabilityOutcome(value=1234567890, constraint_set=self._constraint_sets[1])
        for name, value in self._non_probability_outcome.items():
            with self.subTest(name):
                with self.assertRaises(TypeError):
                    _ = probability_outcome.__equal__(value)

    def test_not_equal(self):
        probability_outcome_one = ProbabilityOutcome(value=1234567890, constraint_set=self._constraint_sets[0])
        probability_outcome_two = ProbabilityOutcome(value=987654321, constraint_set=self._constraint_sets[1])

        new_probability_outcome = probability_outcome_one.__not_equal__(probability_outcome_two)
        self.assertEqual(1, new_probability_outcome.value)
        self.assertEqual(str(self._constraint_sets[-1]), str(new_probability_outcome.constraint_set))

    def test_not_equal_non_probability_outcome(self):
        probability_outcome = ProbabilityOutcome(value=1234567890, constraint_set=self._constraint_sets[1])
        for name, value in self._non_probability_outcome.items():
            with self.subTest(name):
                with self.assertRaises(TypeError):
                    _ = probability_outcome.__not_equal__(value)

    def test_lt(self):
        probability_outcome_one = ProbabilityOutcome(value=1234567890, constraint_set=self._constraint_sets[0])
        probability_outcome_two = ProbabilityOutcome(value=987654321, constraint_set=self._constraint_sets[1])

        new_probability_outcome = probability_outcome_one < probability_outcome_two
        self.assertEqual(1 if 1234567890 < 987654321 else 0, new_probability_outcome.value)
        self.assertEqual(str(self._constraint_sets[-1]), str(new_probability_outcome.constraint_set))

    def test_lt_non_probability_outcome(self):
        probability_outcome = ProbabilityOutcome(value=1234567890, constraint_set=self._constraint_sets[1])
        for name, value in self._non_probability_outcome.items():
            with self.subTest(name):
                with self.assertRaises(TypeError):
                    _ = probability_outcome < value

    def test_le(self):
        probability_outcome_one = ProbabilityOutcome(value=1234567890, constraint_set=self._constraint_sets[0])
        probability_outcome_two = ProbabilityOutcome(value=987654321, constraint_set=self._constraint_sets[1])

        new_probability_outcome = probability_outcome_one <= probability_outcome_two
        self.assertEqual(0, new_probability_outcome.value)
        self.assertEqual(str(self._constraint_sets[-1]), str(new_probability_outcome.constraint_set))

    def test_le_non_probability_outcome(self):
        probability_outcome = ProbabilityOutcome(value=1234567890, constraint_set=self._constraint_sets[1])
        for name, value in self._non_probability_outcome.items():
            with self.subTest(name):
                with self.assertRaises(TypeError):
                    _ = probability_outcome <= value

    def test_gt(self):
        probability_outcome_one = ProbabilityOutcome(value=1234567890, constraint_set=self._constraint_sets[0])
        probability_outcome_two = ProbabilityOutcome(value=987654321, constraint_set=self._constraint_sets[1])

        new_probability_outcome = probability_outcome_one > probability_outcome_two
        self.assertEqual(1, new_probability_outcome.value)
        self.assertEqual(str(self._constraint_sets[-1]), str(new_probability_outcome.constraint_set))

    def test_gt_non_probability_outcome(self):
        probability_outcome = ProbabilityOutcome(value=1234567890, constraint_set=self._constraint_sets[1])
        for name, value in self._non_probability_outcome.items():
            with self.subTest(name):
                with self.assertRaises(TypeError):
                    _ = probability_outcome > value

    def test_ge(self):
        probability_outcome_one = ProbabilityOutcome(value=1234567890, constraint_set=self._constraint_sets[0])
        probability_outcome_two = ProbabilityOutcome(value=987654321, constraint_set=self._constraint_sets[1])

        new_probability_outcome = probability_outcome_one >= probability_outcome_two
        self.assertEqual(1, new_probability_outcome.value)
        self.assertEqual(str(self._constraint_sets[-1]), str(new_probability_outcome.constraint_set))

    def test_ge_non_probability_outcome(self):
        probability_outcome = ProbabilityOutcome(value=1234567890, constraint_set=self._constraint_sets[1])
        for name, value in self._non_probability_outcome.items():
            with self.subTest(name):
                with self.assertRaises(TypeError):
                    _ = probability_outcome >= value

    def test_and(self):
        probability_outcome_one = ProbabilityOutcome(value=1234567890, constraint_set=self._constraint_sets[0])
        probability_outcome_two = ProbabilityOutcome(value=987654321, constraint_set=self._constraint_sets[1])

        new_probability_outcome = probability_outcome_one.__and__(probability_outcome_two)
        self.assertEqual(1, new_probability_outcome.value)
        self.assertEqual(str(self._constraint_sets[-1]), str(new_probability_outcome.constraint_set))

    def test_and_non_probability_outcome(self):
        probability_outcome = ProbabilityOutcome(value=1234567890, constraint_set=self._constraint_sets[1])
        for name, value in self._non_probability_outcome.items():
            with self.subTest(name):
                with self.assertRaises(TypeError):
                    _ = probability_outcome.__and__(value)

    def test_or(self):
        probability_outcome_one = ProbabilityOutcome(value=1234567890, constraint_set=self._constraint_sets[0])
        probability_outcome_two = ProbabilityOutcome(value=987654321, constraint_set=self._constraint_sets[1])

        new_probability_outcome = probability_outcome_one.__or__(probability_outcome_two)
        self.assertEqual(1, new_probability_outcome.value)
        self.assertEqual(str(self._constraint_sets[-1]), str(new_probability_outcome.constraint_set))

    def test_or_non_probability_outcome(self):
        probability_outcome = ProbabilityOutcome(value=1234567890, constraint_set=self._constraint_sets[1])
        for name, value in self._non_probability_outcome.items():
            with self.subTest(name):
                with self.assertRaises(TypeError):
                    _ = probability_outcome.__or__(value)

    @given(integers())
    @settings(deadline=TEST_DEADLINE)
    def test_not(self, value):
        probability_outcome = ProbabilityOutcome(value=value, constraint_set=self._constraint_sets[1])
        abs_probability_outcome = probability_outcome.not_operator()
        self.assertEqual(
            0 if value > 0 else 1,
            abs_probability_outcome.value,
        )

    def test_max_operator(self):
        probability_outcome_one = ProbabilityOutcome(value=1234567890, constraint_set=self._constraint_sets[0])
        probability_outcome_two = ProbabilityOutcome(value=987654321, constraint_set=self._constraint_sets[1])

        new_probability_outcome = probability_outcome_one.max_operator(probability_outcome_two)
        self.assertEqual(max(1234567890, 987654321), new_probability_outcome.value)
        self.assertEqual(str(self._constraint_sets[-1]), str(new_probability_outcome.constraint_set))

    def test_max_operator_non_probability_outcome(self):
        probability_outcome = ProbabilityOutcome(value=1234567890, constraint_set=self._constraint_sets[1])
        for name, value in self._non_probability_outcome.items():
            with self.subTest(name):
                with self.assertRaises(TypeError):
                    _ = probability_outcome.max_operator(value)

    def test_min_operator(self):
        probability_outcome_one = ProbabilityOutcome(value=1234567890, constraint_set=self._constraint_sets[0])
        probability_outcome_two = ProbabilityOutcome(value=987654321, constraint_set=self._constraint_sets[1])

        new_probability_outcome = probability_outcome_one.min_operator(probability_outcome_two)
        self.assertEqual(min(1234567890, 987654321), new_probability_outcome.value)
        self.assertEqual(str(self._constraint_sets[-1]), str(new_probability_outcome.constraint_set))

    def test_min_operator_non_probability_outcome(self):
        probability_outcome = ProbabilityOutcome(value=1234567890, constraint_set=self._constraint_sets[1])
        for name, value in self._non_probability_outcome.items():
            with self.subTest(name):
                with self.assertRaises(TypeError):
                    _ = probability_outcome.min_operator(value)

    @given(integers())
    @settings(deadline=TEST_DEADLINE)
    def test_abs(self, value):
        probability_outcome = ProbabilityOutcome(value=value, constraint_set=self._constraint_sets[1])
        abs_probability_outcome = abs(probability_outcome)
        self.assertEqual(
            abs(value),
            abs_probability_outcome.value,
        )

    @given(integers())
    @settings(deadline=TEST_DEADLINE)
    def test_str(self, value):
        probability_outcome = ProbabilityOutcome(value=value, constraint_set=self._constraint_sets[1])
        self.assertEqual(
            f"ProbabilityOutcome: value={value}, constraint_set={self._constraint_sets[1]}", str(probability_outcome)
        )

    @given(integers())
    @settings(deadline=TEST_DEADLINE)
    def test_repr(self, value):
        probability_outcome = ProbabilityOutcome(value=value, constraint_set=self._constraint_sets[1])
        self.assertEqual(
            f"ProbabilityOutcome: value={value}, constraint_set={self._constraint_sets[1]}", repr(probability_outcome)
        )
