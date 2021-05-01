import copy
import io
import operator
import typing

from matplotlib import pyplot  # type: ignore
from PIL import Image  # type: ignore

from python_dice.interface.probability_distribution.i_probability_distribution import IProbabilityDistribution
from python_dice.interface.probability_distribution.i_probability_outcome import IProbabilityOutcome
from python_dice.interface.probability_distribution.i_probability_outcome_factory import IProbabilityOutcomeFactory


class ProbabilityDistribution(IProbabilityDistribution):
    def __init__(
        self,
        probability_outcome_factory: IProbabilityOutcomeFactory,
        result_map: typing.Optional[typing.Union[typing.Dict[IProbabilityOutcome, int], typing.Dict[int, int]]] = None,
    ):
        self._outcome_count = 0
        self._probability_outcome_factory = probability_outcome_factory
        self._result_map: typing.Dict[IProbabilityOutcome, int] = {}

        def safe_add(key, value):
            if key not in self._result_map:
                self._result_map[key] = 0
            self._result_map[key] += value

        if result_map is not None:
            for result_value, count in result_map.items():
                if isinstance(result_value, int):
                    safe_add(self._probability_outcome_factory.create_empty(value=result_value), count)
                if isinstance(result_value, IProbabilityOutcome):
                    safe_add(result_value, count)
        for value in self._result_map.values():
            self._outcome_count += value

    def get_histogram(self) -> Image:
        histogram_data = self._get_histogram_form(self.get_dict_form())
        x_values = list(histogram_data.keys())
        return self._make_histogram(x_values, [histogram_data[x_value] for x_value in x_values], self.average())

    def get_at_least_histogram(self) -> Image:
        histogram_data = self.at_least()
        x_values = list(histogram_data.keys())
        return self._make_histogram(x_values, [histogram_data[x_value] for x_value in x_values], self.average())

    def get_at_most_histogram(self) -> Image:
        histogram_data = self.at_most()
        x_values = list(histogram_data.keys())
        return self._make_histogram(x_values, [histogram_data[x_value] for x_value in x_values], self.average())

    def get_compare_histogram(self, other_probability: IProbabilityDistribution) -> Image:
        this_histogram_data = self._get_histogram_form(self.get_dict_form())
        other_histogram_data = self._get_histogram_form(other_probability.get_dict_form())
        x_values = list(this_histogram_data.keys())
        x_values.extend(other_histogram_data.keys())

        def y_value_calculator(key):
            value = 0
            if key in this_histogram_data:
                value += this_histogram_data[key]
            if key in other_histogram_data:
                value -= other_histogram_data[key]
            return value

        return self._make_histogram(x_values, [y_value_calculator(x_value) for x_value in x_values])

    def get_compare(
        self,
        other_probability: IProbabilityDistribution,
        this_distribution_name: str = "This distribution",
        other_distribution_name: str = "other distribution",
    ) -> Image:
        this_at_least_data = self._get_histogram_form(self.get_dict_form())
        other_at_least_data = self._get_histogram_form(other_probability.get_dict_form())

        x_values_one = list(this_at_least_data.keys())
        x_values_two = list(other_at_least_data.keys())
        return self._make_line_plot(
            x_values_one,
            [this_at_least_data[x_value] for x_value in x_values_one],
            x_values_two,
            [other_at_least_data[x_value] for x_value in x_values_two],
            this_distribution_name,
            other_distribution_name,
        )

    def get_compare_at_least(
        self,
        other_probability: IProbabilityDistribution,
        this_distribution_name: str = "This distribution",
        other_distribution_name: str = "other distribution",
    ) -> Image:
        this_at_least_data = self.at_least()
        other_at_least_data = other_probability.at_least()

        x_values_one = list(this_at_least_data.keys())
        x_values_two = list(other_at_least_data.keys())
        return self._make_line_plot(
            x_values_one,
            [this_at_least_data[x_value] for x_value in x_values_one],
            x_values_two,
            [other_at_least_data[x_value] for x_value in x_values_two],
            this_distribution_name,
            other_distribution_name,
        )

    def get_compare_at_most(
        self,
        other_probability: IProbabilityDistribution,
        this_distribution_name: str = "This distribution",
        other_distribution_name: str = "other distribution",
    ) -> Image:
        this_at_most_data = self.at_most()
        other_at_most_data = other_probability.at_most()

        x_values_one = list(this_at_most_data.keys())
        x_values_two = list(other_at_most_data.keys())
        return self._make_line_plot(
            x_values_one,
            [this_at_most_data[x_value] for x_value in x_values_one],
            x_values_two,
            [other_at_most_data[x_value] for x_value in x_values_two],
            this_distribution_name,
            other_distribution_name,
        )

    @staticmethod
    def _make_histogram(
        x_values: typing.Union[typing.List[int], typing.List[float]],
        y_values: typing.Union[typing.List[int], typing.List[float]],
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
            max_height = max(y_values)
            axis.plot(
                [average, average],
                [0, max_height * 1.1],
                "-r",
                lw=2,
                label="Average = %d" % average,
            )
        buffer = io.BytesIO()
        pyplot.savefig(buffer, format="tiff")
        buffer.seek(0)
        image = Image.open(buffer)
        return image

    @staticmethod
    def _make_line_plot(
        x_values_one: typing.Union[typing.List[int], typing.List[float]],
        y_values_one: typing.Union[typing.List[int], typing.List[float]],
        x_values_two: typing.Union[typing.List[int], typing.List[float]],
        y_values_two: typing.Union[typing.List[int], typing.List[float]],
        lable_one: str = "Distribution One",
        lable_two: str = "Distribution Two",
    ) -> Image:
        x_values_one, y_values_one = (list(t) for t in zip(*sorted(zip(x_values_one, y_values_one))))
        x_values_two, y_values_two = (list(t) for t in zip(*sorted(zip(x_values_two, y_values_two))))
        _, axis = pyplot.subplots()
        axis.plot(x_values_one, y_values_one, "b", label=lable_one)
        axis.plot(x_values_two, y_values_two, "r", label=lable_two)
        axis.grid(True, linestyle="-.")
        axis.set_ylabel("odds")
        axis.set_xlabel("outcome")
        axis.legend()
        buffer = io.BytesIO()
        pyplot.savefig(buffer, format="png")
        buffer.seek(0)
        image = Image.open(buffer)
        return image

    def max(self) -> int:
        return max(self.get_result_map().keys())

    def min(self) -> int:
        return min(self.get_result_map().keys())

    def contains_zero(self) -> bool:
        result_map = self.get_result_map()
        return 0 in result_map and result_map != 0

    def average(self) -> float:
        total_values = 0
        for item, value in self.get_result_map().items():
            total_values += item * value
        return total_values / self._outcome_count

    def at_least(self) -> typing.Dict[int, float]:
        at_least_dict = {}
        total_above: float = 1
        histogram_form = self._get_histogram_form(self.get_dict_form())
        keys = list(histogram_form.keys())
        keys = sorted(keys)
        for value in keys:
            at_least_dict[value] = total_above / 1
            total_above -= histogram_form[value]
        return at_least_dict

    def at_most(self) -> typing.Dict[int, float]:
        at_most_dict = {}
        at_or_below: float = 0
        histogram_form = self._get_histogram_form(self.get_dict_form())
        keys = list(histogram_form.keys())
        keys = sorted(keys)
        for value in keys:
            at_or_below += histogram_form[value]
            at_most_dict[value] = at_or_below / 1
        return at_most_dict

    def get_result_map(self) -> typing.Dict[int, int]:
        new_result_map = {}

        def safe_add(key, value):
            if key not in new_result_map:
                new_result_map[key] = 0
            new_result_map[key] += value

        for probability_outcome, count in self._result_map.items():
            safe_add(probability_outcome.value, count)
        return new_result_map

    def get_constraint_result_map(self) -> typing.Dict[IProbabilityOutcome, int]:
        return self._result_map

    def get_dict_form(self) -> typing.Dict[int, float]:
        return {key: value / self._outcome_count for key, value in self.get_result_map().items()}

    @staticmethod
    def _get_histogram_form(base_data: typing.Dict[int, float]) -> typing.Dict[int, float]:
        base_data = copy.copy(base_data)
        item_list = [(key, base_data[key]) for key in base_data.keys()]
        item_list.sort(key=lambda tup: tup[0])
        for int_value in range(item_list[0][0], item_list[-1][0] + 1):
            if int_value not in base_data:
                base_data[int_value] = 0
        return base_data

    def _combine_distributions(
        self,
        combination_function: typing.Callable[[IProbabilityOutcome, IProbabilityOutcome], IProbabilityOutcome],
        other: IProbabilityDistribution,
    ) -> typing.Dict[IProbabilityOutcome, int]:
        new_result_map = {}

        def safe_add(key, value):
            if key not in new_result_map:
                new_result_map[key] = 0
            new_result_map[key] += value

        for this_key, this_value in self._result_map.items():
            for other_key, other_value in other.get_constraint_result_map().items():
                new_outcome = combination_function(this_key, other_key)
                if new_outcome.is_possible():
                    safe_add(new_outcome, this_value * other_value)
        return new_result_map

    def __add__(self, other: object) -> IProbabilityDistribution:
        if not isinstance(other, IProbabilityDistribution):
            raise TypeError(f"No __add__ between {ProbabilityDistribution} and {type(other)}")
        new_result_map = self._combine_distributions(operator.add, other)
        return ProbabilityDistribution(self._probability_outcome_factory, new_result_map)

    def __sub__(self, other: object) -> IProbabilityDistribution:
        if not isinstance(other, IProbabilityDistribution):
            raise TypeError(f"No __sub__ between {ProbabilityDistribution} and {type(other)}")
        new_result_map = self._combine_distributions(operator.sub, other)
        return ProbabilityDistribution(self._probability_outcome_factory, new_result_map)

    def __mul__(self, other: object) -> IProbabilityDistribution:
        if not isinstance(other, IProbabilityDistribution):
            raise TypeError(f"No __mul__ between {ProbabilityDistribution} and {type(other)}")
        new_result_map = self._combine_distributions(operator.mul, other)
        return ProbabilityDistribution(self._probability_outcome_factory, new_result_map)

    def __floordiv__(self, other: object) -> IProbabilityDistribution:
        if not isinstance(other, IProbabilityDistribution):
            raise TypeError(f"No __floordiv__ between {ProbabilityDistribution} and {type(other)}")
        new_result_map = self._combine_distributions(operator.floordiv, other)
        return ProbabilityDistribution(self._probability_outcome_factory, new_result_map)

    def __equal__(self, other: object) -> IProbabilityDistribution:
        if not isinstance(other, IProbabilityDistribution):
            raise TypeError(f"No __equal__ between {ProbabilityDistribution} and {type(other)}")
        new_result_map = self._combine_distributions(lambda x, y: x.__equal__(y), other)
        return ProbabilityDistribution(self._probability_outcome_factory, new_result_map)

    def __not_equal__(self, other: object) -> IProbabilityDistribution:
        if not isinstance(other, IProbabilityDistribution):
            raise TypeError(f"No __not_equal__ between {ProbabilityDistribution} and {type(other)}")
        new_result_map = self._combine_distributions(lambda x, y: x.__not_equal__(y), other)
        return ProbabilityDistribution(self._probability_outcome_factory, new_result_map)

    def __lt__(self, other: object) -> IProbabilityDistribution:
        if not isinstance(other, IProbabilityDistribution):
            raise TypeError(f"No __lt__ between {ProbabilityDistribution} and {type(other)}")
        new_result_map = self._combine_distributions(operator.lt, other)
        return ProbabilityDistribution(self._probability_outcome_factory, new_result_map)

    def __le__(self, other: object) -> IProbabilityDistribution:
        if not isinstance(other, IProbabilityDistribution):
            raise TypeError(f"No __le__ between {ProbabilityDistribution} and {type(other)}")
        new_result_map = self._combine_distributions(operator.le, other)
        return ProbabilityDistribution(self._probability_outcome_factory, new_result_map)

    def __gt__(self, other: object) -> IProbabilityDistribution:
        if not isinstance(other, IProbabilityDistribution):
            raise TypeError(f"No __gt__ between {ProbabilityDistribution} and {type(other)}")
        new_result_map = self._combine_distributions(operator.gt, other)
        return ProbabilityDistribution(self._probability_outcome_factory, new_result_map)

    def __ge__(self, other: object) -> IProbabilityDistribution:
        if not isinstance(other, IProbabilityDistribution):
            raise TypeError(f"No __ge__ between {ProbabilityDistribution} and {type(other)}")
        new_result_map = self._combine_distributions(operator.ge, other)
        return ProbabilityDistribution(self._probability_outcome_factory, new_result_map)

    def __and__(self, other: object) -> IProbabilityDistribution:
        if not isinstance(other, IProbabilityDistribution):
            raise TypeError(f"No __and__ between {ProbabilityDistribution} and {type(other)}")
        new_result_map = self._combine_distributions(operator.and_, other)
        return ProbabilityDistribution(self._probability_outcome_factory, new_result_map)

    def __or__(self, other: object) -> IProbabilityDistribution:
        if not isinstance(other, IProbabilityDistribution):
            raise TypeError(f"No __or__ between {ProbabilityDistribution} and {type(other)}")
        new_result_map = self._combine_distributions(operator.or_, other)
        return ProbabilityDistribution(self._probability_outcome_factory, new_result_map)

    def not_operator(self) -> IProbabilityDistribution:
        new_result_map = {}

        def safe_add(key, value):
            if key not in new_result_map:
                new_result_map[key] = 0
            new_result_map[key] += value

        for result_key, result_value in self._result_map.items():
            safe_add(result_key.not_operator(), result_value)
        return ProbabilityDistribution(self._probability_outcome_factory, new_result_map)

    def max_operator(self, other: object) -> IProbabilityDistribution:
        if not isinstance(other, IProbabilityDistribution):
            raise TypeError(f"No max_operator between {ProbabilityDistribution} and {type(other)}")
        new_result_map = self._combine_distributions(lambda x, y: x.max_operator(y), other)
        return ProbabilityDistribution(self._probability_outcome_factory, new_result_map)

    def min_operator(self, other: object) -> IProbabilityDistribution:
        if not isinstance(other, IProbabilityDistribution):
            raise TypeError(f"No min_operator between {ProbabilityDistribution} and {type(other)}")
        new_result_map = self._combine_distributions(lambda x, y: x.min_operator(y), other)
        return ProbabilityDistribution(self._probability_outcome_factory, new_result_map)

    def __abs__(self) -> IProbabilityDistribution:
        new_result_map = {}

        def safe_add(key, value):
            if key not in new_result_map:
                new_result_map[key] = 0
            new_result_map[key] += value

        for result_key, result_value in self._result_map.items():
            safe_add(abs(result_key), result_value)
        return ProbabilityDistribution(self._probability_outcome_factory, new_result_map)

    def __str__(self) -> str:
        return f"{ProbabilityDistribution.__name__}, result_map={self._result_map}"

    def __repr__(self) -> str:
        return self.__str__()
