import typing
import unittest
import unittest.mock as mock

import hypothesis
import hypothesis.strategies as strategies

from python_dice.interface.constraint.i_constraint import IConstraint
from python_dice.src.constraint.impossible_constraint import ImpossibleConstraint


class TestImpossibleConstraint(unittest.TestCase):
    @hypothesis.given(strategies.dictionaries(keys=strategies.text(), values=strategies.sets(strategies.integers())))
    def test_complies(self, var_values: typing.Dict[str, int]):
        constraint = ImpossibleConstraint()
        self.assertTrue(constraint.complies(var_values=var_values))

    def test_can_merge_constraint(self):
        constraint = ImpossibleConstraint()
        merged_constraint = mock.create_autospec(IConstraint)
        self.assertTrue(constraint.can_merge(merged_constraint))

    def test_merge_constraint(self):
        constraint = ImpossibleConstraint()
        merge_constraint = mock.create_autospec(IConstraint)
        self.assertEqual(constraint, constraint.merge(merge_constraint))

    def test_eq_true(self):
        constraint = ImpossibleConstraint()
        second_constraint = ImpossibleConstraint()
        self.assertEqual(constraint, second_constraint)

    def test_eq_false(self):
        constraint = ImpossibleConstraint()
        second_constraint = mock.create_autospec(IConstraint)
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
