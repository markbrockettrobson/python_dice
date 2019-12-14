import copy
import io
import operator
import typing

import matplotlib.pyplot as pyplot
import PIL.Image as Image

import python_dice.interface.i_probability_distribution as i_probability_distribution


class ProbabilityDistribution(i_probability_distribution.IProbabilityDistribution):
    def __init__(self, result_map: typing.Optional[typing.Dict[int, int]] = None):
        self._outcome_count = 0
        self._result_map: typing.Dict[
            int, int
        ] = {} if result_map is None else result_map
        for value in self._result_map.values():
            self._outcome_count += value

    def get_histogram(self) -> Image:
        histogram_data = self._get_histogram_form(self.get_dict_form())
        x_values = list(histogram_data.keys())
        return self._make_histogram(
            x_values, [histogram_data[x_value] for x_value in x_values], self.average()
        )

    def get_at_least_histogram(self) -> Image:
        histogram_data = self.at_least()
        x_values = list(histogram_data.keys())
        return self._make_histogram(
            x_values, [histogram_data[x_value] for x_value in x_values], self.average()
        )

    def get_at_most_histogram(self) -> Image:
        histogram_data = self.at_most()
        x_values = list(histogram_data.keys())
        return self._make_histogram(
            x_values, [histogram_data[x_value] for x_value in x_values], self.average()
        )

    def get_compare_histogram(
        self, other_probability: i_probability_distribution.IProbabilityDistribution
    ) -> Image:
        this_histogram_data = self._get_histogram_form(self.get_dict_form())
        other_histogram_data = self._get_histogram_form(
            other_probability.get_dict_form()
        )
        x_values = list(this_histogram_data.keys())
        x_values.extend(other_histogram_data.keys())

        def y_value_calculator(key):
            value = 0
            if key in this_histogram_data:
                value += this_histogram_data[key]
            if key in other_histogram_data:
                value -= other_histogram_data[key]
            return value

        return self._make_histogram(
            x_values, [y_value_calculator(x_value) for x_value in x_values]
        )

    @staticmethod
    def _make_histogram(
        x_values: typing.List[float],
        y_values: typing.List[float],
        average: float = None,
    ) -> Image:
        x_values, y_values = (list(t) for t in zip(*sorted(zip(x_values, y_values))))
        bins = [value - 0.5 for value in x_values]
        bins.append(x_values[-1] + 0.5)

        _, axis = pyplot.subplots()
        axis.hist(x_values, weights=y_values, bins=bins)
        axis.grid(True, linestyle="-.")
        axis.set_ylabel("odds")
        axis.set_xlabel("outcome")
        if average is not None:
            max_height = max([value for value in y_values])
            axis.plot(
                [average, average],
                [0, max_height * 1.1],
                "-r",
                lw=2,
                label="Average = %d" % average,
            )
        buffer = io.BytesIO()
        pyplot.savefig(buffer, format="png")
        buffer.seek(0)
        image = Image.open(buffer)
        return image

    def max(self) -> int:
        return max(self._result_map.keys())

    def min(self) -> int:
        return min(self._result_map.keys())

    def contains_zero(self) -> bool:
        return 0 in self._result_map and self._result_map[0] != 0

    def average(self) -> float:
        total_values = 0
        for item, value in self._result_map.items():
            total_values += item * value
        return total_values / self._outcome_count

    def at_least(self) -> typing.Dict[int, float]:
        at_least_dict = {}
        total_above = 1
        histogram_form = self._get_histogram_form(self.get_dict_form())
        keys = list(histogram_form.keys())
        keys = sorted(keys)
        for value in keys:
            at_least_dict[value] = total_above / 1
            total_above -= histogram_form[value]
        return at_least_dict

    def at_most(self) -> typing.Dict[int, float]:
        at_most_dict = {}
        at_or_below = 0
        histogram_form = self._get_histogram_form(self.get_dict_form())
        keys = list(histogram_form.keys())
        keys = sorted(keys)
        for value in keys:
            at_or_below += histogram_form[value]
            at_most_dict[value] = at_or_below / 1
        return at_most_dict

    def get_result_map(self) -> typing.Dict[int, int]:
        return self._result_map

    def get_dict_form(self) -> typing.Dict[int, float]:
        return {
            key: value / self._outcome_count for key, value in self._result_map.items()
        }

    @staticmethod
    def _get_histogram_form(
        base_data: typing.Dict[int, float]
    ) -> typing.Dict[int, float]:
        base_data = copy.copy(base_data)
        item_list = [item for item in base_data.items()]
        item_list.sort(key=lambda tup: tup[0])
        for int_value in range(item_list[0][0], item_list[-1][0] + 1):
            if int_value not in base_data:
                base_data[int_value] = 0
        return base_data

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
        return ProbabilityDistribution(new_result_map)

    def __sub__(
        self, other: i_probability_distribution.IProbabilityDistribution
    ) -> "ProbabilityDistribution":
        new_result_map = self._combine_distributions(operator.sub, other)
        return ProbabilityDistribution(new_result_map)

    def __mul__(
        self, other: i_probability_distribution.IProbabilityDistribution
    ) -> "ProbabilityDistribution":
        new_result_map = self._combine_distributions(operator.mul, other)
        return ProbabilityDistribution(new_result_map)

    def __floordiv__(
        self, other: i_probability_distribution.IProbabilityDistribution
    ) -> "ProbabilityDistribution":
        new_result_map = self._combine_distributions(operator.floordiv, other)
        return ProbabilityDistribution(new_result_map)

    def __eq__(
        self, other: i_probability_distribution.IProbabilityDistribution
    ) -> "ProbabilityDistribution":
        new_result_map = self._combine_distributions(
            lambda a, b: 1 if operator.eq(a, b) else 0, other
        )
        return ProbabilityDistribution(new_result_map)

    def __ne__(
        self, other: i_probability_distribution.IProbabilityDistribution
    ) -> "ProbabilityDistribution":
        new_result_map = self._combine_distributions(
            lambda a, b: 1 if operator.ne(a, b) else 0, other
        )
        return ProbabilityDistribution(new_result_map)

    def __lt__(
        self, other: i_probability_distribution.IProbabilityDistribution
    ) -> "ProbabilityDistribution":
        new_result_map = self._combine_distributions(
            lambda a, b: 1 if operator.lt(a, b) else 0, other
        )
        return ProbabilityDistribution(new_result_map)

    def __le__(
        self, other: i_probability_distribution.IProbabilityDistribution
    ) -> "ProbabilityDistribution":
        new_result_map = self._combine_distributions(
            lambda a, b: 1 if operator.le(a, b) else 0, other
        )
        return ProbabilityDistribution(new_result_map)

    def __gt__(
        self, other: i_probability_distribution.IProbabilityDistribution
    ) -> "ProbabilityDistribution":
        new_result_map = self._combine_distributions(
            lambda a, b: 1 if operator.gt(a, b) else 0, other
        )
        return ProbabilityDistribution(new_result_map)

    def __ge__(
        self, other: i_probability_distribution.IProbabilityDistribution
    ) -> "ProbabilityDistribution":
        new_result_map = self._combine_distributions(
            lambda a, b: 1 if operator.ge(a, b) else 0, other
        )
        return ProbabilityDistribution(new_result_map)

    def __and__(
        self, other: i_probability_distribution.IProbabilityDistribution
    ) -> "ProbabilityDistribution":
        new_result_map = self._combine_distributions(
            lambda a, b: 1 if operator.and_(a, b) else 0, other
        )
        return ProbabilityDistribution(new_result_map)

    def __or__(
        self, other: i_probability_distribution.IProbabilityDistribution
    ) -> "ProbabilityDistribution":
        new_result_map = self._combine_distributions(
            lambda a, b: 1 if operator.or_(a, b) else 0, other
        )
        return ProbabilityDistribution(new_result_map)

    def not_operator(self) -> "ProbabilityDistribution":
        new_result_map = {}

        def safe_add(key, value):
            if key not in new_result_map:
                new_result_map[key] = 0
            new_result_map[key] += value

        for result_key, result_value in self._result_map.items():
            if result_key:
                safe_add(0, result_value)
            else:
                safe_add(1, result_value)
        return ProbabilityDistribution(new_result_map)

    def max_operator(
        self, other: "ProbabilityDistribution"
    ) -> "ProbabilityDistribution":
        new_result_map = {}

        def safe_add(key, value):
            if key not in new_result_map:
                new_result_map[key] = 0
            new_result_map[key] += value

        for result_key, result_value in self._result_map.items():
            for other_result_key, other_result_value in other.get_result_map().items():
                safe_add(
                    max(result_key, other_result_key), result_value * other_result_value
                )
        return ProbabilityDistribution(new_result_map)

    def min_operator(
        self, other: "ProbabilityDistribution"
    ) -> "ProbabilityDistribution":
        new_result_map = {}

        def safe_add(key, value):
            if key not in new_result_map:
                new_result_map[key] = 0
            new_result_map[key] += value

        for result_key, result_value in self._result_map.items():
            for other_result_key, other_result_value in other.get_result_map().items():
                safe_add(
                    min(result_key, other_result_key), result_value * other_result_value
                )
        return ProbabilityDistribution(new_result_map)

    def abs_operator(self) -> "ProbabilityDistribution":
        new_result_map = {}

        def safe_add(key, value):
            if key not in new_result_map:
                new_result_map[key] = 0
            new_result_map[key] += value

        for result_key, result_value in self._result_map.items():
            safe_add(abs(result_key), result_value)
        return ProbabilityDistribution(new_result_map)
