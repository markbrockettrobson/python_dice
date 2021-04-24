import typing

from python_dice.interface.probability_distribution.i_probability_distribution import IProbabilityDistribution
from python_dice.interface.probability_distribution.i_probability_distribution_state import (
    IProbabilityDistributionState,
)


class ProbabilityDistributionState(IProbabilityDistributionState):
    def get_var_dict(self):
        return self._var

    def get_constant_dict(self):
        return self._constants

    def __init__(self):
        self._var: typing.Dict[str, IProbabilityDistribution] = {}
        self._constants: typing.Dict[str, int] = {}

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

    def set_var(
        self,
        name: str,
        distribution: IProbabilityDistribution,
    ) -> None:
        self._var[name] = distribution
