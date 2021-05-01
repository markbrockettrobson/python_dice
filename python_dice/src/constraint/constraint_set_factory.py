import typing

from python_dice.interface.constraint.i_constraint_factory import IConstraintFactory
from python_dice.interface.constraint.i_constraint_merger import IConstraintMerger
from python_dice.interface.constraint.i_constraint_set import IConstraintSet
from python_dice.interface.constraint.i_constraint_set_factory import IConstraintSetFactory
from python_dice.src.constraint.constraint_factory import ConstraintFactory
from python_dice.src.constraint.constraint_merger import ConstraintMerger
from python_dice.src.constraint.constraint_set import ConstraintSet


class ConstraintSetFactory(IConstraintSetFactory):
    def __init__(
        self,
        constraint_factory: typing.Optional[IConstraintFactory] = None,
        constraint_merger: typing.Optional[IConstraintMerger] = None,
    ):
        if constraint_merger is not None:
            self._constraint_merger = constraint_merger
        else:
            self._constraint_merger = ConstraintMerger()

        if constraint_factory is not None:
            self._constraint_factory = constraint_factory
        else:
            self._constraint_factory = ConstraintFactory()

    def create_constraint_set(self) -> IConstraintSet:
        return ConstraintSet({self._constraint_factory.null_constraint}, self._constraint_merger)
