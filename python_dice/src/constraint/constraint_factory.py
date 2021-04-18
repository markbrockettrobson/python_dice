import typing

from python_dice.interface.constraint.i_constraint import IConstraint
from python_dice.interface.constraint.i_constraint_factory import IConstraintFactory
from python_dice.interface.constraint.i_var_value_constraint import IVarValueConstraint
from python_dice.src.constraint.impossible_constraint import ImpossibleConstraint
from python_dice.src.constraint.null_constraint import NullConstraint
from python_dice.src.constraint.var_value_constraint import VarValueConstraint


class ConstraintFactory(IConstraintFactory):
    def __init__(self):
        self.__null_constraint = NullConstraint()
        self.__impossible_constraint = ImpossibleConstraint()

    @property
    def impossible_constraint(self) -> IConstraint:
        return self.__impossible_constraint

    @property
    def null_constraint(self) -> IConstraint:
        return self.__null_constraint

    def var_value_constraint(self, name: str, values: typing.Set[int]) -> IVarValueConstraint:
        return VarValueConstraint(name=name, values=values, constraint_factory=self)
