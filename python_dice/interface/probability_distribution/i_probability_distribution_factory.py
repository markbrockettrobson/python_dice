from abc import ABC, abstractmethod
from typing import Dict, Optional, Union

from python_dice.interface.probability_distribution.i_probability_distribution import IProbabilityDistribution
from python_dice.interface.probability_distribution.i_probability_outcome import IProbabilityOutcome


class IProbabilityDistributionFactory(ABC):
    @abstractmethod
    def create(
        self,
        result_map: Optional[Union[Dict[IProbabilityOutcome, int], Dict[int, int]]] = None,
    ) -> IProbabilityDistribution:
        pass
