from unittest import TestCase
from unittest.mock import create_autospec

from python_dice.interface.constraint.i_constraint_factory import IConstraintFactory
from python_dice.interface.constraint.i_constraint_merger import IConstraintMerger
from python_dice.interface.constraint.i_constraint_set import IConstraintSet
from python_dice.src.constraint.constraint_set_factory import ConstraintSetFactory


class TestConstraintSetFactory(TestCase):
    def test_create_constraint_set(self):
        constraint_set_factory = ConstraintSetFactory()
        self.assertIsInstance(constraint_set_factory.create_constraint_set(), IConstraintSet)

    @staticmethod
    def test_uses_constraint_merger():
        mock_constraint_merger = create_autospec(IConstraintMerger)
        constraint_set_factory = ConstraintSetFactory(constraint_merger=mock_constraint_merger)
        constraint_set_factory.create_constraint_set()
        mock_constraint_merger.merge_new_constraints.assert_called_once()

    def test_uses_constraint_factory(self):
        mock_constraint_factory = create_autospec(IConstraintFactory)
        constraint_set_factory = ConstraintSetFactory(constraint_factory=mock_constraint_factory)
        new_set = constraint_set_factory.create_constraint_set()
        self.assertEqual({mock_constraint_factory.null_constraint}, set(new_set.constraints))
