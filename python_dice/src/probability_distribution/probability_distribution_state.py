import copy
from typing import Dict

from python_dice.interface.constraint.i_constraint_factory import IConstraintFactory
from python_dice.interface.probability_distribution.i_probability_distribution import IProbabilityDistribution
from python_dice.interface.probability_distribution.i_probability_distribution_factory import (
    IProbabilityDistributionFactory,
)
from python_dice.interface.probability_distribution.i_probability_distribution_state import (
    IProbabilityDistributionState,
)


class ProbabilityDistributionState(IProbabilityDistributionState):
    def __init__(
        self, probability_distribution_factory: IProbabilityDistributionFactory, constraint_factory: IConstraintFactory
    ):
        self._var: Dict[str, IProbabilityDistribution] = {}
        self._constants: Dict[str, int] = {}
        self._number_of_times_set: Dict[str, int] = {}
        self._probability_distribution_factory = probability_distribution_factory
        self._constraint_factory = constraint_factory

    def get_var_dict(self):
        return self._var

    def get_constant_dict(self):
        return self._constants

    def has_constant(self, name) -> bool:
        return name in self._constants

    def has_var(self, name: str) -> bool:
        return name in self._var

    def get_constant(self, name: str) -> int:
        if not self.has_constant(name):
            raise KeyError(f"Constant named {name} not in state.")
        return self._constants[name]

    def get_var(self, name: str) -> IProbabilityDistribution:
        if not self.has_var(name):
            raise KeyError(f"Var named {name} not in state.")
        return self._var[name]

    def set_constant(self, name: str, value: int) -> None:
        self._constants[name] = value
        if name not in self._number_of_times_set:
            self._number_of_times_set[name] = 0
        self._number_of_times_set[name] += 1

    def set_var(
        self,
        name: str,
        distribution: IProbabilityDistribution,
    ) -> None:
        if name not in self._number_of_times_set:
            self._number_of_times_set[name] = 0
        self._number_of_times_set[name] += 1

        new_name = f"{name}_{self._number_of_times_set[name]}"
        new_probability_outcomes = {}
        for old_probability_outcome, count in distribution.get_constraint_result_map().items():
            new_constraint = self._constraint_factory.var_value_constraint(
                name=new_name, values={old_probability_outcome.value}
            )
            new_probability_outcome = copy.deepcopy(old_probability_outcome)
            new_probability_outcome.constraint_set.add_constraint(new_constraint)
            new_probability_outcomes[new_probability_outcome] = count
        self._var[name] = self._probability_distribution_factory.create(new_probability_outcomes)
