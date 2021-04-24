import typing
import unittest
import unittest.mock as mock

import hypothesis
import hypothesis.strategies as strategies

from python_dice.interface.constraint.i_constraint import IConstraint
from python_dice.interface.constraint.i_constraint_merger import IConstraintMerger
from python_dice.src.constraint.constraint_set import ConstraintSet


class TestConstraintSet(unittest.TestCase):
    def setUp(self):
        self._constraint_merger = mock.create_autospec(IConstraintMerger)
        self._mock_constraints = [mock.create_autospec(IConstraint) for _ in range(10)]

        for constraint in self._mock_constraints:
            constraint.complies.return_value = True

        self._constraint_merger.merge_new_constraints.return_value = set(self._mock_constraints)

    def test_empty_add_constraint(self):
        constraint_set = ConstraintSet(self._constraint_merger)
        constraint_set.add_constraint(self._mock_constraints[0])

    def test_add_constraint_calls_constraint_merger(self):
        self._constraint_merger.merge_new_constraints.return_value = set(self._mock_constraints[-1:])

        constraint_set = ConstraintSet(self._constraint_merger)
        for constraint in self._mock_constraints[0:4]:
            constraint_set.add_constraint(constraint)
        calls = [mock.call(constraint_set=set(), new_constraint=self._mock_constraints[0])]
        calls.extend(
            [
                mock.call(constraint_set={self._mock_constraints[-1]}, new_constraint=self._mock_constraints[index])
                for index in range(1, 4)
            ]
        )

        self._constraint_merger.merge_new_constraints.assert_has_calls(calls)

    def test_constraints(self):
        mock_set = mock.Mock()
        self._constraint_merger.merge_new_constraints.return_value = mock_set

        constraint_set = ConstraintSet(self._constraint_merger)
        for constraint in self._mock_constraints[0:4]:
            constraint_set.add_constraint(constraint)

        self.assertEqual(constraint_set.constraints, mock_set.copy())

    def test_combine_sets(self):
        mock_sets = [
            {self._mock_constraints[0]},
            {self._mock_constraints[1]},
            {self._mock_constraints[2]},
            {self._mock_constraints[3]},
        ]
        self._constraint_merger.merge_new_constraints.side_effect = mock_sets

        constraint_set_one = ConstraintSet(self._constraint_merger)
        constraint_set_two = ConstraintSet(self._constraint_merger)
        constraint_set_one.add_constraint(self._mock_constraints[0])
        constraint_set_two.add_constraint(self._mock_constraints[0])

        constraint_set = constraint_set_one.combine_sets(constraint_set_two)
        self.assertEqual(constraint_set.constraints, mock_sets[-1].copy())

    @hypothesis.given(
        var_values=strategies.dictionaries(keys=strategies.text(), values=strategies.sets(strategies.integers())),
    )
    def test_empty_complies(self, var_values: typing.Dict[str, int]):
        constraint_set = ConstraintSet(self._constraint_merger)
        self.assertTrue(constraint_set.complies(var_values=var_values))

    @hypothesis.given(
        var_values=strategies.dictionaries(keys=strategies.text(), values=strategies.sets(strategies.integers())),
    )
    def test_complies_true(self, var_values: typing.Dict[str, int]):
        for constraint in self._mock_constraints:
            constraint.reset_mock()

        constraint_set = ConstraintSet(self._constraint_merger)
        for constraint in self._mock_constraints:
            constraint_set.add_constraint(constraint)

        self.assertTrue(constraint_set.complies(var_values=var_values))
        for constraint in self._mock_constraints:
            constraint.complies.assert_called_once_with(var_values=var_values)

    @hypothesis.given(
        var_values=strategies.dictionaries(keys=strategies.text(), values=strategies.sets(strategies.integers())),
        false_indies=strategies.sets(strategies.integers(min_value=0, max_value=9), min_size=1),
    )
    def test_complies_false(self, var_values: typing.Dict[str, int], false_indies: typing.Set[int]):
        for constraint in self._mock_constraints:
            constraint.reset_mock()

        for false_index in false_indies:
            self._mock_constraints[false_index].complies.return_value = False
        constraint_set = ConstraintSet(self._constraint_merger)
        for constraint in self._mock_constraints:
            constraint_set.add_constraint(constraint)

        self.assertFalse(constraint_set.complies(var_values=var_values))

    def test_empty_eq(self):
        constraint_set_one = ConstraintSet(self._constraint_merger)
        constraint_set_two = ConstraintSet(self._constraint_merger)

        self.assertEqual(constraint_set_one, constraint_set_two)

    def test_eq_true(self):
        constraint_set_one = ConstraintSet(self._constraint_merger)
        constraint_set_two = ConstraintSet(self._constraint_merger)

        constraint_set_one.add_constraint(self._mock_constraints[0])
        constraint_set_two.add_constraint(self._mock_constraints[0])

        self.assertTrue(constraint_set_one == constraint_set_two)

    def test_eq_false(self):
        self._constraint_merger.merge_new_constraints.side_effect = [
            set(self._mock_constraints[0:2:]),
            set(self._mock_constraints[1:2:]),
        ]

        constraint_set_one = ConstraintSet(self._constraint_merger)
        constraint_set_two = ConstraintSet(self._constraint_merger)

        constraint_set_one.add_constraint(self._mock_constraints[0])
        constraint_set_two.add_constraint(self._mock_constraints[0])

        self.assertFalse(constraint_set_one == constraint_set_two)

    def test_ne_false(self):
        constraint_set_one = ConstraintSet(self._constraint_merger)
        constraint_set_two = ConstraintSet(self._constraint_merger)

        constraint_set_one.add_constraint(self._mock_constraints[0])
        constraint_set_two.add_constraint(self._mock_constraints[0])

        self.assertFalse(constraint_set_one != constraint_set_two)

    def test_ne_true(self):
        self._constraint_merger.merge_new_constraints.side_effect = [
            set(self._mock_constraints[0:2:]),
            set(self._mock_constraints[1:2:]),
        ]

        constraint_set_one = ConstraintSet(self._constraint_merger)
        constraint_set_two = ConstraintSet(self._constraint_merger)

        constraint_set_one.add_constraint(self._mock_constraints[0])
        constraint_set_two.add_constraint(self._mock_constraints[0])

        self.assertTrue(constraint_set_one, constraint_set_two)

    def test_empty_str(self):
        constraint_set = ConstraintSet(self._constraint_merger)

        self.assertEqual("ConstraintSet: set()", str(constraint_set))

    def test_str(self):
        constraint_set = ConstraintSet(self._constraint_merger)
        constraint_set.add_constraint(self._mock_constraints[0])

        self.assertEqual(f"ConstraintSet: {set(self._mock_constraints)}", str(constraint_set))

    def test_repr(self):
        constraint_set = ConstraintSet(self._constraint_merger)
        constraint_set.add_constraint(self._mock_constraints[0])

        self.assertEqual(f"ConstraintSet: {set(self._mock_constraints)}", repr(constraint_set))
