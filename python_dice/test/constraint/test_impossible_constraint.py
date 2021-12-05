from typing import Dict
from unittest import TestCase
from unittest.mock import create_autospec

from hypothesis import given, settings
from hypothesis.strategies import dictionaries, integers, sets, text

from python_dice.interface.constraint.i_constraint import IConstraint
from python_dice.src.constraint.impossible_constraint import ImpossibleConstraint


class TestImpossibleConstraint(TestCase):
    TEST_DEADLINE = 2000

    @given(dictionaries(keys=text(), values=sets(integers())))
    @settings(deadline=TEST_DEADLINE)
    def test_complies(self, var_values: Dict[str, int]):
        constraint = ImpossibleConstraint()
        self.assertTrue(constraint.complies(var_values=var_values))

    def test_can_merge_constraint(self):
        constraint = ImpossibleConstraint()
        merged_constraint = create_autospec(IConstraint)
        self.assertTrue(constraint.can_merge(merged_constraint))

    def test_merge_constraint(self):
        constraint = ImpossibleConstraint()
        merge_constraint = create_autospec(IConstraint)
        self.assertEqual(constraint, constraint.merge(merge_constraint))

    def test_is_possible(self):
        constraint = ImpossibleConstraint()
        self.assertEqual(False, constraint.is_possible())

    def test_eq_true(self):
        constraint = ImpossibleConstraint()
        second_constraint = ImpossibleConstraint()
        self.assertEqual(constraint, second_constraint)

    def test_eq_false(self):
        constraint = ImpossibleConstraint()
        second_constraint = create_autospec(IConstraint)
        second_constraint.__str__.return_value = "Mock str"
        self.assertNotEqual(constraint, second_constraint)

    def test_str(self):
        constraint = ImpossibleConstraint()
        self.assertEqual("ImpossibleConstraint", str(constraint))

    def test_repr(self):
        constraint = ImpossibleConstraint()
        self.assertEqual("ImpossibleConstraint", repr(constraint))

    def test_hash_equal(self):
        constraint_one = ImpossibleConstraint()
        constraint_two = ImpossibleConstraint()
        self.assertEqual(hash(constraint_one), hash(constraint_two))
