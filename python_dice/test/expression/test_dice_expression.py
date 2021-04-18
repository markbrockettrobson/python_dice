import collections
import itertools
import unittest
import unittest.mock as mock

import rply  # type: ignore

from python_dice.src.expression.dice_expression import DiceExpression


# pylint: disable=too-many-public-methods
class TestDiceExpression(unittest.TestCase):
    def setUp(self):
        self._test_dice = DiceExpression("4d6")
        self._mock_parser_gen = mock.create_autospec(rply.ParserGenerator)

    def test_dice_add_production_function(self):
        DiceExpression.add_production_function(self._mock_parser_gen)
        self._mock_parser_gen.production.assert_called_once_with("""expression : DICE""")

    def test_dice_roll(self):
        self._test_dice = DiceExpression("2d10")
        roll_set = set()
        for _ in range(1000):
            roll_set.add(self._test_dice.roll())
        self.assertEqual(19, len(roll_set))
        self.assertEqual(20, max(roll_set))
        self.assertEqual(2, min(roll_set))

    def test_dice_roll_missing_dice_amount(self):
        self._test_dice = DiceExpression("d10")
        roll_set = set()
        for _ in range(1000):
            roll_set.add(self._test_dice.roll())
        self.assertEqual(10, len(roll_set))
        self.assertEqual(10, max(roll_set))
        self.assertEqual(1, min(roll_set))

    def test_dice_roll_percentile_dice(self):
        self._test_dice = DiceExpression("1d%")
        roll_set = set()
        for _ in range(10000):
            roll_set.add(self._test_dice.roll())
        self.assertEqual(100, len(roll_set))
        self.assertEqual(100, max(roll_set))
        self.assertEqual(1, min(roll_set))

    def test_dice_roll_fate_dice(self):
        self._test_dice = DiceExpression("2dF")
        roll_set = set()
        for _ in range(10000):
            roll_set.add(self._test_dice.roll())
        self.assertSetEqual(roll_set, {-2, -1, 0, 1, 2})

    def test_dice_roll_custom_dice_negative(self):
        self._test_dice = DiceExpression("2d[-2,2,100]")
        roll_set = set()
        for _ in range(10000):
            roll_set.add(self._test_dice.roll())
        self.assertSetEqual(roll_set, {-4, 0, 4, 98, 102, 200})

    def test_dice_roll_custom_dice_large_set(self):
        self._test_dice = DiceExpression("2d[-2,0,2,4,6,31]")
        roll_set = set()
        for _ in range(10000):
            roll_set.add(self._test_dice.roll())
        self.assertSetEqual(roll_set, {-4, -2, 0, 2, 4, 6, 8, 10, 12, 29, 31, 33, 35, 37, 62})

    def test_dice_max(self):
        self.assertEqual(24, self._test_dice.max())

    def test_dice_max_missing_dice_amount(self):
        self._test_dice = DiceExpression("d10")
        self.assertEqual(10, self._test_dice.max())

    def test_dice_max_percentile_dice(self):
        self._test_dice = DiceExpression("1d%")
        self.assertEqual(100, self._test_dice.max())

    def test_dice_max_fate_dice(self):
        self._test_dice = DiceExpression("2dF")
        self.assertEqual(2, self._test_dice.max())

    def test_dice_max_custom_dice_negative(self):
        self._test_dice = DiceExpression("21d[-2,2,100]")
        self.assertEqual(2100, self._test_dice.max())

    def test_dice_max_custom_dice_large_set(self):
        self._test_dice = DiceExpression("76d[-2,0,2,4,6,31]")
        self.assertEqual(2356, self._test_dice.max())

    def test_dice_min(self):
        self.assertEqual(4, self._test_dice.min())

    def test_dice_min_missing_dice_amount(self):
        self._test_dice = DiceExpression("d10")
        self.assertEqual(1, self._test_dice.min())

    def test_dice_min_percentile_dice(self):
        self._test_dice = DiceExpression("1d%")
        self.assertEqual(1, self._test_dice.min())

    def test_dice_min_fate_dice(self):
        self._test_dice = DiceExpression("4dF")
        self.assertEqual(-4, self._test_dice.min())

    def test_dice_min_custom_dice_negative(self):
        self._test_dice = DiceExpression("21d[-2,2,100]")
        self.assertEqual(-42, self._test_dice.min())

    def test_dice_min_custom_dice_large_set(self):
        self._test_dice = DiceExpression("d[-2,0,2,4,6,31,-2,-24]")
        self.assertEqual(-24, self._test_dice.min())

    def test_dice_str(self):
        self.assertEqual("4d6", str(self._test_dice))

    def test_dice_str_missing_dice_amount(self):
        self._test_dice = DiceExpression("d10")
        self.assertEqual("d10", str(self._test_dice))

    def test_dice_str_percentile_dice(self):
        self._test_dice = DiceExpression("1d%")
        self.assertEqual("1d%", str(self._test_dice))

    def test_dice_str_fate_dice(self):
        self._test_dice = DiceExpression("4dF")
        self.assertEqual("4dF", str(self._test_dice))

    def test_dice_str_custom_dice_negative(self):
        self._test_dice = DiceExpression("21d[-2,2,100]")
        self.assertEqual("21d[-2,2,100]", str(self._test_dice))

    def test_dice_str_custom_dice_large_set(self):
        self._test_dice = DiceExpression("d[-2,0,2,4,6,31,-2,-24]")
        self.assertEqual("d[-2,0,2,4,6,31,-2,-24]", str(self._test_dice))

    def test_dice_estimated_cost(self):
        self.assertEqual(4 * 6, self._test_dice.estimated_cost())

    def test_dice_estimated_cost_missing_dice_amount(self):
        self._test_dice = DiceExpression("d10")
        self.assertEqual(10, self._test_dice.estimated_cost())

    def test_dice_estimated_cost_percentile_dice(self):
        self._test_dice = DiceExpression("1d%")
        self.assertEqual(100, self._test_dice.estimated_cost())

    def test_dice_estimated_cost_fate_dice(self):
        self._test_dice = DiceExpression("10dF")
        self.assertEqual(30, self._test_dice.estimated_cost())

    def test_dice_estimated_custom_dice_negative(self):
        self._test_dice = DiceExpression("21d[-2,2,100]")
        self.assertEqual(63, self._test_dice.estimated_cost())

    def test_dice_estimated_custom_dice_large_set(self):
        self._test_dice = DiceExpression("2d[-2,0,2,4,6*7,31,-2,-24]")
        self.assertEqual(14, self._test_dice.estimated_cost())

    def test_dice_get_probability_distribution(self):
        self._test_dice = DiceExpression("4d6")
        possible_rolls = itertools.product(range(1, 7), repeat=4)
        results = [sum(t) for t in possible_rolls]
        self.assertEqual(
            dict(collections.Counter(results)),
            self._test_dice.get_probability_distribution().get_result_map(),
        )

    def test_dice_get_probability_distribution_missing_dice_amount(self):
        self._test_dice = DiceExpression("d10")
        possible_rolls = itertools.product(range(1, 11), repeat=1)
        results = [sum(t) for t in possible_rolls]
        self.assertEqual(
            dict(collections.Counter(results)),
            self._test_dice.get_probability_distribution().get_result_map(),
        )

    def test_dice_get_probability_distribution_percentile_dice(self):
        self._test_dice = DiceExpression("2d%")
        possible_rolls = itertools.product(range(1, 101), repeat=2)
        results = [sum(t) for t in possible_rolls]
        self.assertEqual(
            dict(collections.Counter(results)),
            self._test_dice.get_probability_distribution().get_result_map(),
        )

    def test_dice_get_probability_distribution_fate_dice(self):
        self._test_dice = DiceExpression("4dF")
        self.assertEqual(
            {-4: 1, -3: 4, -2: 10, -1: 16, 0: 19, 1: 16, 2: 10, 3: 4, 4: 1},
            self._test_dice.get_probability_distribution().get_result_map(),
        )

    def test_dice_get_probability_distribution_custom_dice_negative(self):
        self._test_dice = DiceExpression("2d[-2,2,100]")
        self.assertEqual(
            {-4: 1, 0: 2, 4: 1, 98: 2, 102: 2, 200: 1},
            self._test_dice.get_probability_distribution().get_result_map(),
        )

    def test_dice_get_probability_distribution_custom_dice_large_set(self):
        self._test_dice = DiceExpression("d[-2,0,2,4,6,31,-2,-24]")
        self.assertEqual(
            {-24: 1, -2: 2, 0: 1, 2: 1, 4: 1, 6: 1, 31: 1},
            self._test_dice.get_probability_distribution().get_result_map(),
        )

    def test_dice_get_probability_distribution_custom_dice_multiplier(self):
        self._test_dice = DiceExpression("d[-2*3,0,2]")
        self.assertEqual(
            {-2: 3, 0: 1, 2: 1},
            self._test_dice.get_probability_distribution().get_result_map(),
        )

    def test_dice_get_probability_distribution_custom_dice_range(self):
        self._test_dice = DiceExpression("d[1-2*3,0,2]")
        self.assertEqual(
            {0: 1, 1: 3, 2: 4},
            self._test_dice.get_probability_distribution().get_result_map(),
        )

    def test_dice_get_probability_distribution_custom_dice_multiplier_range(self):
        self._test_dice = DiceExpression("d[1-2*3,-4--9*10]")
        self.assertEqual(
            {-9: 10, -8: 10, -7: 10, -6: 10, -5: 10, -4: 10, 1: 3, 2: 3},
            self._test_dice.get_probability_distribution().get_result_map(),
        )

    def test_dice_get_contained_variables(self):
        self.assertSetEqual(set(), self._test_dice.get_contained_variables())
