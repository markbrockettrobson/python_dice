from typing import List
from unittest import TestCase
from unittest.mock import create_autospec

from hypothesis import given, settings
from hypothesis.strategies import integers, lists

from python_dice.interface.constraint.i_constraint import IConstraint
from python_dice.src.constraint.constraint_merger import ConstraintMerger


class TestConstraintMerger(TestCase):
    TEST_SIZE = 6
    TEST_DEADLINE = 2000

    def setUp(self):
        self._mock_constraints = [create_autospec(IConstraint) for _ in range(self.TEST_SIZE)]
        for constraint in self._mock_constraints:
            constraint.can_merge.return_value = False

    def _set_up_single_merge(self, index_one: int, index_two: int):
        self._merged_constraint = create_autospec(IConstraint)
        self._merged_constraint.can_merge.return_value = False

        self._mock_constraints[index_one].can_merge.side_effect = (
            lambda constraint: constraint == self._mock_constraints[index_two]
        )
        self._mock_constraints[index_one].merge.return_value = self._merged_constraint

    def _set_up_chain_merge(self, index_one: int, index_two: int, index_three: int, index_four: int):
        self._merged_constraints = [create_autospec(IConstraint) for _ in range(3)]
        for merged_constraint in self._merged_constraints:
            merged_constraint.can_merge.return_value = False

        self._mock_constraints[index_one].can_merge.side_effect = (
            lambda constraint: constraint == self._mock_constraints[index_two]
        )
        self._merged_constraints[0].can_merge.side_effect = (
            lambda constraint: constraint == self._mock_constraints[index_three]
        )
        self._merged_constraints[1].can_merge.side_effect = (
            lambda constraint: constraint == self._mock_constraints[index_four]
        )

        self._mock_constraints[index_one].merge.return_value = self._merged_constraints[0]
        self._merged_constraints[0].merge.return_value = self._merged_constraints[1]
        self._merged_constraints[1].merge.return_value = self._merged_constraints[2]

    def _set_up_tree_merge(self, index_one: int, index_two: int, index_three: int, index_four: int, index_five: int):
        self._merged_constraints = [create_autospec(IConstraint) for _ in range(4)]

        self._mock_constraints[index_one].can_merge.side_effect = (
            lambda constraint: constraint == self._mock_constraints[index_two]
        )
        self._mock_constraints[index_three].can_merge.side_effect = (
            lambda constraint: constraint == self._mock_constraints[index_four]
        )
        self._mock_constraints[index_five].can_merge.side_effect = (
            lambda constraint: constraint == self._merged_constraints[2]
        )
        self._merged_constraints[0].can_merge.side_effect = lambda constraint: constraint == self._merged_constraints[1]
        self._merged_constraints[1].can_merge.return_value = False
        self._merged_constraints[2].can_merge.return_value = False
        self._merged_constraints[3].can_merge.return_value = False

        self._mock_constraints[index_one].merge.return_value = self._merged_constraints[0]
        self._mock_constraints[index_three].merge.return_value = self._merged_constraints[1]
        self._mock_constraints[index_five].merge.return_value = self._merged_constraints[3]
        self._merged_constraints[0].merge.return_value = self._merged_constraints[2]

    def test_merge_constraints_no_merge(self):
        constraint_merger = ConstraintMerger()
        self.assertEqual(constraint_merger.merge_constraints(set(self._mock_constraints)), set(self._mock_constraints))

    @given(new_constraint_index=integers(min_value=0, max_value=TEST_SIZE - 1))
    @settings(deadline=TEST_DEADLINE)
    def test_merge_constraints_no_merge_new_constraints_add_one(self, new_constraint_index: int):
        constraint_merger = ConstraintMerger()
        self.assertEqual(
            constraint_merger.merge_new_constraints(
                set(self._mock_constraints) - {self._mock_constraints[new_constraint_index]},
                self._mock_constraints[new_constraint_index],
            ),
            set(self._mock_constraints),
        )

    @given(indexes=lists(integers(min_value=0, max_value=TEST_SIZE - 1), min_size=2, max_size=2, unique=True))
    @settings(deadline=TEST_DEADLINE)
    def test_merge_constraints_single_merge(self, indexes: List[int]):
        self.setUp()
        self._set_up_single_merge(index_one=indexes[0], index_two=indexes[1])

        constraint_merger = ConstraintMerger()

        expected_set = set(self._mock_constraints)
        expected_set.add(self._merged_constraint)
        expected_set.remove(self._mock_constraints[indexes[0]])
        expected_set.remove(self._mock_constraints[indexes[1]])

        self.assertEqual(constraint_merger.merge_constraints(set(self._mock_constraints)), expected_set)

    @given(indexes=lists(integers(min_value=0, max_value=TEST_SIZE - 1), min_size=3, max_size=3, unique=True))
    @settings(deadline=TEST_DEADLINE)
    def test_merge_new_constraints_single_merge_in_old_set(self, indexes: List[int]):
        self.setUp()
        self._set_up_single_merge(index_one=indexes[0], index_two=indexes[1])
        constraint_merger = ConstraintMerger()

        test_set = set(self._mock_constraints)
        test_set.remove(self._mock_constraints[indexes[2]])

        expected_set = set(self._mock_constraints)

        self.assertEqual(
            constraint_merger.merge_new_constraints(test_set, self._mock_constraints[indexes[2]]), expected_set
        )

    @given(indexes=lists(integers(min_value=0, max_value=TEST_SIZE - 1), min_size=2, max_size=2, unique=True))
    @settings(deadline=TEST_DEADLINE)
    def test_merge_new_constraints_single_merge_in_new_value(self, indexes: List[int]):
        self.setUp()
        self._set_up_single_merge(index_one=indexes[0], index_two=indexes[1])
        constraint_merger = ConstraintMerger()

        input_set = set(self._mock_constraints)
        input_set.remove(self._mock_constraints[indexes[0]])

        expected_set = set(self._mock_constraints)
        expected_set.add(self._merged_constraint)
        expected_set.remove(self._mock_constraints[indexes[0]])
        expected_set.remove(self._mock_constraints[indexes[1]])

        self.assertEqual(
            constraint_merger.merge_new_constraints(input_set, self._mock_constraints[indexes[0]]), expected_set
        )

    @given(indexes=lists(integers(min_value=0, max_value=TEST_SIZE - 1), min_size=4, max_size=4, unique=True))
    @settings(deadline=TEST_DEADLINE)
    def test_merge_constraints_chain_merge(self, indexes: List[int]):
        self.setUp()
        self._set_up_chain_merge(
            index_one=indexes[0], index_two=indexes[1], index_three=indexes[2], index_four=indexes[3]
        )
        constraint_merger = ConstraintMerger()

        expected_set = set(self._mock_constraints)
        expected_set.add(self._merged_constraints[2])
        expected_set.remove(self._mock_constraints[indexes[0]])
        expected_set.remove(self._mock_constraints[indexes[1]])
        expected_set.remove(self._mock_constraints[indexes[2]])
        expected_set.remove(self._mock_constraints[indexes[3]])

        self.assertEqual(constraint_merger.merge_constraints(set(self._mock_constraints)), expected_set)

    @given(indexes=lists(integers(min_value=0, max_value=TEST_SIZE - 1), min_size=5, max_size=5, unique=True))
    @settings(deadline=TEST_DEADLINE)
    def test_merge_new_constraints_chain_in_old_set(self, indexes: List[int]):
        self.setUp()
        self._set_up_chain_merge(
            index_one=indexes[0], index_two=indexes[1], index_three=indexes[2], index_four=indexes[3]
        )
        constraint_merger = ConstraintMerger()

        test_set = set(self._mock_constraints)
        test_set.remove(self._mock_constraints[indexes[4]])

        expected_set = set(self._mock_constraints)

        self.assertEqual(
            constraint_merger.merge_new_constraints(test_set, self._mock_constraints[indexes[4]]), expected_set
        )

    @given(indexes=lists(integers(min_value=0, max_value=TEST_SIZE - 1), min_size=4, max_size=4, unique=True))
    @settings(deadline=TEST_DEADLINE)
    def test_merge_new_constraints_chain_merge_in_new_value(self, indexes: List[int]):
        self.setUp()
        self._set_up_chain_merge(
            index_one=indexes[0], index_two=indexes[1], index_three=indexes[2], index_four=indexes[3]
        )
        constraint_merger = ConstraintMerger()

        input_set = set(self._mock_constraints)
        input_set.remove(self._mock_constraints[indexes[0]])

        expected_set = set(self._mock_constraints)
        expected_set.add(self._merged_constraints[2])
        expected_set.remove(self._mock_constraints[indexes[0]])
        expected_set.remove(self._mock_constraints[indexes[1]])
        expected_set.remove(self._mock_constraints[indexes[2]])
        expected_set.remove(self._mock_constraints[indexes[3]])

        self.assertEqual(
            constraint_merger.merge_new_constraints(input_set, self._mock_constraints[indexes[0]]), expected_set
        )

    @given(indexes=lists(integers(min_value=0, max_value=TEST_SIZE - 1), min_size=5, max_size=5, unique=True))
    @settings(deadline=TEST_DEADLINE)
    def test_merge_constraints_tree_merge(self, indexes: List[int]):
        self.setUp()
        self._set_up_tree_merge(
            index_one=indexes[0],
            index_two=indexes[1],
            index_three=indexes[2],
            index_four=indexes[3],
            index_five=indexes[4],
        )
        constraint_merger = ConstraintMerger()

        expected_set = set(self._mock_constraints)
        expected_set.add(self._merged_constraints[3])
        expected_set.remove(self._mock_constraints[indexes[0]])
        expected_set.remove(self._mock_constraints[indexes[1]])
        expected_set.remove(self._mock_constraints[indexes[2]])
        expected_set.remove(self._mock_constraints[indexes[3]])
        expected_set.remove(self._mock_constraints[indexes[4]])

        self.assertEqual(constraint_merger.merge_constraints(set(self._mock_constraints)), expected_set)

    @given(indexes=lists(integers(min_value=0, max_value=TEST_SIZE - 1), min_size=6, max_size=6, unique=True))
    @settings(deadline=TEST_DEADLINE)
    def test_merge_new_constraints_tree_in_old_set(self, indexes: List[int]):
        self.setUp()
        self._set_up_tree_merge(
            index_one=indexes[0],
            index_two=indexes[1],
            index_three=indexes[2],
            index_four=indexes[3],
            index_five=indexes[4],
        )
        constraint_merger = ConstraintMerger()

        test_set = set(self._mock_constraints)
        test_set.remove(self._mock_constraints[indexes[5]])

        expected_set = set(self._mock_constraints)

        self.assertEqual(
            constraint_merger.merge_new_constraints(test_set, self._mock_constraints[indexes[5]]), expected_set
        )

    @given(indexes=lists(integers(min_value=0, max_value=TEST_SIZE - 1), min_size=5, max_size=5, unique=True))
    @settings(deadline=TEST_DEADLINE)
    def test_merge_new_constraints_tree_merge_in_new_value(self, indexes: List[int]):
        self.setUp()
        self._set_up_tree_merge(
            index_one=indexes[0],
            index_two=indexes[1],
            index_three=indexes[2],
            index_four=indexes[3],
            index_five=indexes[4],
        )
        constraint_merger = ConstraintMerger()

        input_set = set(self._mock_constraints)
        input_set.remove(self._mock_constraints[indexes[0]])

        expected_set = set(self._mock_constraints)
        expected_set.add(self._merged_constraints[0])
        expected_set.remove(self._mock_constraints[indexes[0]])
        expected_set.remove(self._mock_constraints[indexes[1]])
        self.assertEqual(
            constraint_merger.merge_new_constraints(input_set, self._mock_constraints[indexes[0]]), expected_set
        )

    def test_str(self):
        constraint_merger = ConstraintMerger()
        self.assertEqual("ConstraintMerger", str(constraint_merger))

    def test_repr(self):
        constraint_merger = ConstraintMerger()
        self.assertEqual("ConstraintMerger", repr(constraint_merger))
