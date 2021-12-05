from typing import Set
from unittest import TestCase

from hypothesis import given, settings
from hypothesis.strategies import integers, sets, text

from python_dice.interface.constraint.i_impossible_constraint import IImpossibleConstraint
from python_dice.interface.constraint.i_null_constraint import INullConstraint
from python_dice.interface.constraint.i_var_value_constraint import IVarValueConstraint
from python_dice.src.constraint.constraint_factory import ConstraintFactory


class TestConstraintFactory(TestCase):
    TEST_DEADLINE = 2000

    def test_impossible_constraint(self):
        constraint_factory = ConstraintFactory()
        self.assertIsInstance(constraint_factory.impossible_constraint, IImpossibleConstraint)

    def test_null_constraint(self):
        constraint_factory = ConstraintFactory()
        self.assertIsInstance(constraint_factory.null_constraint, INullConstraint)

    @given(name=text(), int_set=sets(integers()))
    @settings(deadline=TEST_DEADLINE)
    def test_var_value_constraint(self, name: str, int_set: Set[int]):
        constraint_factory = ConstraintFactory()
        var_value_constraint = constraint_factory.var_value_constraint(name=name, values=int_set)

        self.assertIsInstance(var_value_constraint, IVarValueConstraint)
        self.assertEqual(var_value_constraint.name, name)
        self.assertEqual(var_value_constraint.values, int_set)
