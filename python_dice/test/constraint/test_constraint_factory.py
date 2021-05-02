from typing import Set
from unittest import TestCase

import hypothesis
import hypothesis.strategies as strategies

from python_dice.interface.constraint.i_impossible_constraint import IImpossibleConstraint
from python_dice.interface.constraint.i_null_constraint import INullConstraint
from python_dice.interface.constraint.i_var_value_constraint import IVarValueConstraint
from python_dice.src.constraint.constraint_factory import ConstraintFactory


class TestConstraintFactory(TestCase):
    def test_impossible_constraint(self):
        constraint_factory = ConstraintFactory()
        self.assertIsInstance(constraint_factory.impossible_constraint, IImpossibleConstraint)

    def test_null_constraint(self):
        constraint_factory = ConstraintFactory()
        self.assertIsInstance(constraint_factory.null_constraint, INullConstraint)

    @hypothesis.given(name=strategies.text(), int_set=strategies.sets(strategies.integers()))
    @hypothesis.settings(deadline=1000)
    def test_var_value_constraint(self, name: str, int_set: Set[int]):
        constraint_factory = ConstraintFactory()
        var_value_constraint = constraint_factory.var_value_constraint(name=name, values=int_set)

        self.assertIsInstance(var_value_constraint, IVarValueConstraint)
        self.assertEqual(var_value_constraint.name, name)
        self.assertEqual(var_value_constraint.values, int_set)
