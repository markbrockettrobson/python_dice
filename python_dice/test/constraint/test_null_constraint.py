from typing import Dict
from unittest import TestCase
from unittest.mock import create_autospec

from hypothesis import given, settings
from hypothesis.strategies import dictionaries, integers, sets, text

from python_dice.interface.constraint.i_constraint import IConstraint
from python_dice.src.constraint.null_constraint import NullConstraint


class TestNullConstraint(TestCase):
    TEST_DEADLINE = 2000

    @given(dictionaries(keys=text(), values=sets(integers())))
    @settings(deadline=TEST_DEADLINE)
    def test_complies(self, var_values: Dict[str, int]):
        constraint = NullConstraint()
        self.assertTrue(constraint.complies(var_values=var_values))

    def test_can_merge_constraint(self):
        constraint = NullConstraint()
        merged_constraint = create_autospec(IConstraint)
        self.assertTrue(constraint.can_merge(merged_constraint))

    def test_is_possible(self):
        constraint = NullConstraint()
        self.assertEqual(True, constraint.is_possible())

    def test_merge_constraint(self):
        constraint = NullConstraint()
        merge_constraint = create_autospec(IConstraint)
        self.assertEqual(merge_constraint, constraint.merge(merge_constraint))

    def test_eq_true(self):
        constraint = NullConstraint()
        second_constraint = NullConstraint()
        self.assertEqual(constraint, second_constraint)

    def test_eq_false(self):
        constraint = NullConstraint()
        second_constraint = create_autospec(IConstraint)
        second_constraint.__str__.return_value = "Mock str"
        self.assertNotEqual(constraint, second_constraint)

    def test_str(self):
        constraint = NullConstraint()
        self.assertEqual("NullConstraint", str(constraint))

    def test_repr(self):
        constraint = NullConstraint()
        self.assertEqual("NullConstraint", repr(constraint))

    def test_hash_equal(self):
        constraint_one = NullConstraint()
        constraint_two = NullConstraint()
        self.assertEqual(hash(constraint_one), hash(constraint_two))
