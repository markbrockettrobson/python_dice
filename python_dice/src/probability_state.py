import typing

import python_dice.interface.i_probability_distribution as i_probability_distribution
import python_dice.interface.i_probability_state as i_probability_state


class ProbabilityState(i_probability_state.IProbabilityDistributionState):
    def __init__(self):
        self._var: typing.Dict[
            str, i_probability_distribution.IProbabilityDistribution
        ] = {}
        self._constants: typing.Dict[str, int] = {}

    def has_constant(self, name) -> bool:
        return name in self._constants

    def has_var(self, name: str) -> bool:
        return name in self._var

    def get_constant(self, name: str) -> int:
        if not self.has_constant(name):
            raise KeyError(f"Constant named {name} not in state.")
        return self._constants[name]

    def get_var(self, name: str) -> i_probability_distribution.IProbabilityDistribution:
        if not self.has_var(name):
            raise KeyError(f"Var named {name} not in state.")
        return self._var[name]

    def set_constant(self, name: str, value: int) -> None:
        self._constants[name] = value

    def set_var(
        self,
        name: str,
        distribution: i_probability_distribution.IProbabilityDistribution,
    ) -> None:
        self._var[name] = distribution
