import operator
from typing import Callable

from python_dice.interface.constraint.i_constraint_set import IConstraintSet
from python_dice.interface.probability_distribution.i_probability_outcome import IProbabilityOutcome


class ProbabilityOutcome(IProbabilityOutcome):
    def __init__(self, value: int, constraint_set: IConstraintSet):
        if not isinstance(value, int):
            raise TypeError("can not have a bool value for a probability outcome")

        self._value = value
        self._constraint_set = constraint_set

    @property
    def value(self) -> int:
        return self._value

    @property
    def constraint_set(self) -> IConstraintSet:
        return self._constraint_set

    def _combine(
        self,
        combination_function: Callable[[int, int], int],
        other: object,
        binary_values: bool = False,
    ) -> IProbabilityOutcome:
        if not isinstance(other, IProbabilityOutcome):
            raise TypeError(
                f"No {combination_function.__name__} between {ProbabilityOutcome.__name__} and {type(other)}."
            )
        if binary_values:
            new_value = combination_function(
                self._value_to_binary_value(self.value), self._value_to_binary_value(other.value)
            )
        else:
            new_value = combination_function(self.value, other.value)

        if isinstance(new_value, bool):
            new_value = self._binary_to_int(new_value)
        new_constraint_set = self._constraint_set.combine_sets(other.constraint_set)
        return ProbabilityOutcome(value=new_value, constraint_set=new_constraint_set)

    def is_possible(self) -> bool:
        return self._constraint_set.is_possible()

    @staticmethod
    def _value_to_binary_value(value: int) -> int:
        return value > 0

    @staticmethod
    def _binary_to_int(value: bool) -> int:
        return 1 if value else 0

    def __add__(self, other: object) -> IProbabilityOutcome:
        return self._combine(combination_function=operator.add, other=other)

    def __sub__(self, other: object) -> IProbabilityOutcome:
        return self._combine(combination_function=operator.sub, other=other)

    def __mul__(self, other: object) -> IProbabilityOutcome:
        return self._combine(combination_function=operator.mul, other=other)

    def __floordiv__(self, other: object) -> IProbabilityOutcome:
        return self._combine(combination_function=operator.floordiv, other=other)

    def __equal__(self, other: object) -> IProbabilityOutcome:
        return self._combine(combination_function=operator.eq, other=other)

    def __not_equal__(self, other: object) -> IProbabilityOutcome:
        return self._combine(combination_function=operator.ne, other=other)

    def __lt__(self, other: object) -> IProbabilityOutcome:
        return self._combine(combination_function=operator.lt, other=other)

    def __le__(self, other: object) -> IProbabilityOutcome:
        return self._combine(combination_function=operator.le, other=other)

    def __gt__(self, other: object) -> IProbabilityOutcome:
        return self._combine(combination_function=operator.gt, other=other)

    def __ge__(self, other: object) -> IProbabilityOutcome:
        return self._combine(combination_function=operator.ge, other=other)

    def __and__(self, other: object) -> IProbabilityOutcome:
        return self._combine(combination_function=operator.and_, other=other, binary_values=True)

    def __or__(self, other: object) -> IProbabilityOutcome:
        return self._combine(combination_function=operator.or_, other=other, binary_values=True)

    def not_operator(self) -> IProbabilityOutcome:
        new_value = 0 if self._value_to_binary_value(self.value) else 1
        return ProbabilityOutcome(value=new_value, constraint_set=self._constraint_set)

    def max_operator(self, other: object) -> IProbabilityOutcome:
        return self._combine(combination_function=max, other=other)

    def min_operator(self, other: object) -> IProbabilityOutcome:
        return self._combine(combination_function=min, other=other)

    def __abs__(self) -> IProbabilityOutcome:
        return ProbabilityOutcome(value=abs(self.value), constraint_set=self._constraint_set)

    def __str__(self) -> str:
        return f"{ProbabilityOutcome.__name__}: value={self.value}, constraint_set={self.constraint_set}"

    def __repr__(self) -> str:
        return self.__str__()

    def __hash__(self) -> int:
        return operator.xor(
            hash(ProbabilityOutcome.__name__), operator.xor(hash(self.value), hash(self.constraint_set))
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, IProbabilityOutcome):
            raise TypeError(f"No == between {ProbabilityOutcome.__name__} and {type(other)}.")
        return self.value == other.value and self.constraint_set == other.constraint_set
