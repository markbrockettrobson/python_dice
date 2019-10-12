import typing
import operator
import matplotlib.pyplot as pyplot

import python_dice.interface.i_probability_distribution as i_probability_distribution


class ProbabilityDistribution(i_probability_distribution.IProbabilityDistribution):
    def __init__(self):
        self._outcome_count = 0
        self._result_map: typing.Dict[int, int] = {}

    @classmethod
    def build_form_result_map(cls, result_map: typing.Dict[int, int]):
        distribution = ProbabilityDistribution()
        for key, value in result_map.items():
            distribution._result_map[key] = value
            distribution._outcome_count += value
        return distribution

    def show_histogram(self) -> None:
        item_list = [item for item in self._get_show_histogram_form().items()]
        item_list.sort(key=lambda tup: tup[0])
        y_values = [value for _, value in item_list]
        x_values = [key for key, _ in item_list]
        bins = [key - 0.5 for key, _ in item_list]
        bins.append(item_list[-1][0] + 0.5)

        figure, axis = pyplot.subplots()
        axis.hist(x_values, weights=y_values, bins=bins)
        axis.grid(True, linestyle="-.")
        figure.show()

    def get_result_map(self) -> typing.Dict[int, int]:
        return self._result_map

    def get_dict_form(self) -> typing.Dict[int, float]:
        return {
            key: value / self._outcome_count for key, value in self._result_map.items()
        }

    def _get_show_histogram_form(self) -> typing.Dict[int, float]:
        dict_data = self.get_dict_form()
        item_list = [item for item in dict_data.items()]
        item_list.sort(key=lambda tup: tup[0])
        for int_value in range(item_list[0][0], item_list[-1][0] + 1):
            if int_value not in dict_data:
                dict_data[int_value] = 0
        return dict_data

    def _combine_distributions(
        self,
        combination_function: typing.Callable[[int, int], int],
        other: i_probability_distribution.IProbabilityDistribution,
    ) -> typing.Dict[int, int]:
        new_result_map = {}

        def safe_add(key, value):
            if key not in new_result_map:
                new_result_map[key] = 0
            new_result_map[key] += value

        for this_key, this_value in self._result_map.items():
            for other_key, other_value in other.get_result_map().items():
                safe_add(
                    combination_function(this_key, other_key), this_value * other_value
                )
        return new_result_map

    def __add__(
        self, other: i_probability_distribution.IProbabilityDistribution
    ) -> "ProbabilityDistribution":
        new_result_map = self._combine_distributions(operator.add, other)
        return ProbabilityDistribution.build_form_result_map(new_result_map)

    def __sub__(
        self, other: i_probability_distribution.IProbabilityDistribution
    ) -> "ProbabilityDistribution":
        new_result_map = self._combine_distributions(operator.sub, other)
        return ProbabilityDistribution.build_form_result_map(new_result_map)

    def __mul__(
        self, other: i_probability_distribution.IProbabilityDistribution
    ) -> "ProbabilityDistribution":
        new_result_map = self._combine_distributions(operator.mul, other)
        return ProbabilityDistribution.build_form_result_map(new_result_map)

    def __floordiv__(
        self, other: i_probability_distribution.IProbabilityDistribution
    ) -> "ProbabilityDistribution":
        new_result_map = self._combine_distributions(operator.floordiv, other)
        return ProbabilityDistribution.build_form_result_map(new_result_map)
