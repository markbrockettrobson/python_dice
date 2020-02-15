import itertools
from collections import Counter

import unittest
import unittest.mock as mock

import rply

import python_dice.src.python_dice_expression.dice_expression as dice_expression


class TestDiceExpression(unittest.TestCase):
    def setUp(self):
        self._test_dice = dice_expression.DiceExpression("4d6")
        self._test_dice_no_dice_amount = dice_expression.DiceExpression("d10")
        self._test_percentile_die = dice_expression.DiceExpression("1d%")
        self._mock_parser_gen = mock.create_autospec(rply.ParserGenerator)

    def test_dice_add_production_function(self):
        dice_expression.DiceExpression.add_production_function(self._mock_parser_gen)
        self._mock_parser_gen.production.assert_called_once_with(
            """expression : DICE"""
        )

    def test_dice_roll(self):
        # Test regular dice syntax
        self._test_dice = dice_expression.DiceExpression("2d10")
        roll_set = set()
        for _ in range(1000):
            roll_set.add(self._test_dice.roll())
        self.assertEqual(19, len(roll_set))
        self.assertEqual(20, max(roll_set))
        self.assertEqual(2, min(roll_set))

        # Test missing dice amount syntax (i.e. "d10")
        roll_set = set()
        for _ in range(1000):
            roll_set.add(self._test_dice_no_dice_amount.roll())
        self.assertEqual(10, len(roll_set))
        self.assertEqual(10, max(roll_set))
        self.assertEqual(1, min(roll_set))

        # Test percentile die syntax (i.e. "1d%")
        roll_set = set()
        for _ in range(10000):
            roll_set.add(self._test_percentile_die.roll())
        self.assertEqual(100, len(roll_set))
        self.assertEqual(100, max(roll_set))
        self.assertEqual(1, min(roll_set))

    def test_dice_max(self):
        self.assertEqual(24, self._test_dice.max())
        self.assertEqual(10, self._test_dice_no_dice_amount.max())
        self.assertEqual(100, self._test_percentile_die.max())

    def test_dice_min(self):
        self.assertEqual(4, self._test_dice.min())
        self.assertEqual(1, self._test_dice_no_dice_amount.min())
        self.assertEqual(1, self._test_percentile_die.min())

    def test_dice_str(self):
        self.assertEqual("4d6", str(self._test_dice))
        self.assertEqual("d10", str(self._test_dice_no_dice_amount))
        self.assertEqual("1d%", str(self._test_percentile_die))

    def test_dice_get_probability_distribution(self):
        self._test_dice = dice_expression.DiceExpression("4d6")
        possible_rolls = itertools.product(range(1, 7), repeat = 4)
        results = [sum(t) for t in possible_rolls]
        self.assertEqual(
            dict(Counter(results)),
            self._test_dice.get_probability_distribution().get_result_map()
        )

        possible_rolls = itertools.product(range(1, 11), repeat = 1)
        results = [sum(t) for t in possible_rolls]
        self.assertEqual(
            dict(Counter(results)),
            self._test_dice_no_dice_amount.get_probability_distribution().get_result_map()
        )

        self._test_percentile_dice = dice_expression.DiceExpression("2d%")
        possible_rolls = itertools.product(range(1, 101), repeat = 2)
        results = [sum(t) for t in possible_rolls]
        self.assertEqual(
            dict(Counter(results)),
            self._test_percentile_dice.get_probability_distribution().get_result_map()
        )
