import typing

from python_dice.interface.constraint.i_constraint import IConstraint
from python_dice.interface.constraint.i_constraint_factory import IConstraintFactory
from python_dice.interface.constraint.i_var_value_constraint import IVarValueConstraint


class VarValueConstraint(IVarValueConstraint):
    def __init__(self, name: str, values: typing.Set[int], constraint_factory: IConstraintFactory):
        self._name = name
        self._values = values
        self._constraint_factory = constraint_factory

    @property
    def name(self) -> str:
        return self._name

    @property
    def values(self) -> typing.Set[int]:
        return self._values

    def complies(self, var_values: typing.Dict[str, int]) -> bool:
        if self._name in var_values:
            if var_values[self._name] not in self._values:
                return False
        return True

    def can_merge(self, other: IConstraint) -> bool:
        if isinstance(other, IVarValueConstraint):
            return other.name == self._name
        return False

    def merge(self, other: IConstraint) -> IConstraint:
        if not self.can_merge(other):
            raise ValueError(f"can not merge {str(other)} with {self.__str__()}")

        if isinstance(other, IVarValueConstraint):
            common_values = self._values.intersection(other.values)

            if len(common_values) == 0:
                return self._constraint_factory.impossible_constraint
            return self._constraint_factory.var_value_constraint(name=self._name, values=common_values)

        raise ValueError(f"can not merge {str(other)} with {self.__str__()} however can_merge returned true")

    def __hash__(self) -> int:
        return hash(self.__str__())

    def __eq__(self, other: object) -> bool:
        return str(self) == str(other)

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __str__(self) -> str:
        return f"{VarValueConstraint.__name__}: name={self._name}, values={self._values}"

    def __repr__(self) -> str:
        return self.__str__()
