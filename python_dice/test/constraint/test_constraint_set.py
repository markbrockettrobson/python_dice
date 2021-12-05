from typing import Dict, Set
from unittest import TestCase
from unittest.mock import Mock, call, create_autospec

from hypothesis import given, settings
from hypothesis.strategies import dictionaries, integers, sets, text

from python_dice.interface.constraint.i_constraint import IConstraint
from python_dice.interface.constraint.i_constraint_merger import IConstraintMerger
from python_dice.src.constraint.constraint_set import ConstraintSet


class TestConstraintSet(TestCase):
    TEST_DEADLINE = 2000

    def setUp(self):
        self._constraint_merger = create_autospec(IConstraintMerger)
        self._mock_constraints = [create_autospec(IConstraint) for _ in range(10)]

        for constraint in self._mock_constraints:
            constraint.complies.return_value = True
            constraint.is_possible.return_value = True

        self._constraint_merger.merge_new_constraints.return_value = set(self._mock_constraints)

    def test_empty_constraint(self):
        with self.assertRaises(ValueError):
            _ = ConstraintSet(set(), self._constraint_merger)

    def test_add_constraint_calls_constraint_merger(self):
        self._constraint_merger.merge_new_constraints.return_value = set(self._mock_constraints[-1:])

        constraint_set = ConstraintSet({self._mock_constraints[0]}, self._constraint_merger)
        for constraint in self._mock_constraints[1:4]:
            constraint_set.add_constraint(constraint)
        calls = [call(constraint_set=set(), new_constraint=self._mock_constraints[0])]
        calls.extend(
            [
                call(constraint_set={self._mock_constraints[-1]}, new_constraint=self._mock_constraints[index])
                for index in range(1, 4)
            ]
        )

        self._constraint_merger.merge_new_constraints.assert_has_calls(calls)

    def test_constraints(self):
        mock_set = Mock()
        self._constraint_merger.merge_new_constraints.return_value = mock_set

        constraint_set = ConstraintSet({self._mock_constraints[0]}, self._constraint_merger)
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

        constraint_set_one = ConstraintSet({self._mock_constraints[0]}, self._constraint_merger)
        constraint_set_two = ConstraintSet({self._mock_constraints[0]}, self._constraint_merger)

        constraint_set = constraint_set_one.combine_sets(constraint_set_two)
        self.assertEqual(constraint_set.constraints, mock_sets[-1].copy())

    @given(
        var_values=dictionaries(keys=text(), values=sets(integers())),
    )
    @settings(deadline=TEST_DEADLINE)
    def test_complies_true(self, var_values: Dict[str, int]):
        for constraint in self._mock_constraints:
            constraint.reset_mock()

        constraint_set = ConstraintSet({self._mock_constraints[0]}, self._constraint_merger)
        for constraint in self._mock_constraints:
            constraint_set.add_constraint(constraint)

        self.assertTrue(constraint_set.complies(var_values=var_values))
        for constraint in self._mock_constraints:
            constraint.complies.assert_called_once_with(var_values=var_values)

    @given(
        var_values=dictionaries(keys=text(), values=sets(integers())),
        false_indies=sets(integers(min_value=0, max_value=9), min_size=1),
    )
    @settings(deadline=TEST_DEADLINE)
    def test_complies_false(self, var_values: Dict[str, int], false_indies: Set[int]):
        for constraint in self._mock_constraints:
            constraint.reset_mock()

        for false_index in false_indies:
            self._mock_constraints[false_index].complies.return_value = False
        constraint_set = ConstraintSet(set(self._mock_constraints), self._constraint_merger)

        self.assertFalse(constraint_set.complies(var_values=var_values))

    def test_is_possible_true(self):
        constraint_set = ConstraintSet({self._mock_constraints[0]}, self._constraint_merger)
        self.assertTrue(constraint_set.is_possible())

    @given(
        false_indies=sets(integers(min_value=0, max_value=9), min_size=1),
    )
    @settings(deadline=TEST_DEADLINE)
    def test_is_possible_false(self, false_indies: Set[int]):
        for constraint in self._mock_constraints:
            constraint.reset_mock()
        for false_index in false_indies:
            self._mock_constraints[false_index].is_possible.return_value = False
        constraint_set = ConstraintSet(set(self._mock_constraints), self._constraint_merger)
        self.assertFalse(constraint_set.is_possible())

    def test_eq_true(self):
        constraint_set_one = ConstraintSet({self._mock_constraints[0]}, self._constraint_merger)
        constraint_set_two = ConstraintSet({self._mock_constraints[0]}, self._constraint_merger)

        constraint_set_one.add_constraint(self._mock_constraints[0])
        constraint_set_two.add_constraint(self._mock_constraints[0])

        self.assertTrue(constraint_set_one == constraint_set_two)

    def test_eq_false(self):
        self._constraint_merger.merge_new_constraints.side_effect = [
            set(self._mock_constraints[0:2:]),
            set(self._mock_constraints[1:2:]),
        ]

        constraint_set_one = ConstraintSet({self._mock_constraints[0]}, self._constraint_merger)
        constraint_set_two = ConstraintSet({self._mock_constraints[0]}, self._constraint_merger)

        self.assertFalse(constraint_set_one == constraint_set_two)

    def test_ne_false(self):
        constraint_set_one = ConstraintSet({self._mock_constraints[0]}, self._constraint_merger)
        constraint_set_two = ConstraintSet({self._mock_constraints[0]}, self._constraint_merger)

        self.assertFalse(constraint_set_one != constraint_set_two)

    def test_ne_true(self):
        self._constraint_merger.merge_new_constraints.side_effect = [
            set(self._mock_constraints[0:2:]),
            set(self._mock_constraints[1:2:]),
        ]

        constraint_set_one = ConstraintSet({self._mock_constraints[0]}, self._constraint_merger)
        constraint_set_two = ConstraintSet({self._mock_constraints[0]}, self._constraint_merger)

        self.assertTrue(constraint_set_one, constraint_set_two)

    def test_str(self):
        constraint_set = ConstraintSet({self._mock_constraints[0]}, self._constraint_merger)
        constraint_set.add_constraint(self._mock_constraints[0])

        self.assertEqual(f"ConstraintSet: {set(self._mock_constraints)}", str(constraint_set))

    def test_repr(self):
        constraint_set = ConstraintSet({self._mock_constraints[0]}, self._constraint_merger)
        constraint_set.add_constraint(self._mock_constraints[0])

        self.assertEqual(f"ConstraintSet: {set(self._mock_constraints)}", repr(constraint_set))

    def test_hash_same(self):
        constraint_set_one = ConstraintSet(
            {self._mock_constraints[0], self._mock_constraints[1]}, self._constraint_merger
        )
        constraint_set_two = ConstraintSet(
            {self._mock_constraints[0], self._mock_constraints[1]}, self._constraint_merger
        )

        self.assertEqual(hash(constraint_set_one), hash(constraint_set_two))

    def test_hash_same_order_different(self):
        constraint_set_one = ConstraintSet(
            {self._mock_constraints[1], self._mock_constraints[0]}, self._constraint_merger
        )
        constraint_set_two = ConstraintSet(
            {self._mock_constraints[0], self._mock_constraints[1]}, self._constraint_merger
        )

        self.assertEqual(hash(constraint_set_one), hash(constraint_set_two))

    def test_hash_different_constraints(self):
        mock_set_one = {self._mock_constraints[0], self._mock_constraints[1]}
        mock_set_two = {self._mock_constraints[1], self._mock_constraints[2]}

        self._constraint_merger.merge_new_constraints.side_effect = [
            mock_set_one,
            mock_set_one,
            mock_set_two,
            mock_set_two,
        ]

        constraint_set_one = ConstraintSet(mock_set_one, self._constraint_merger)
        constraint_set_two = ConstraintSet(mock_set_two, self._constraint_merger)

        self.assertNotEqual(hash(constraint_set_one), hash(constraint_set_two))
