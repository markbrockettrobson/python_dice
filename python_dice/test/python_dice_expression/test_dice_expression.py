import unittest
import unittest.mock as mock

import rply

import python_dice.src.python_dice_expression.dice_expression as dice_expression


class TestDiceExpression(unittest.TestCase):
    def setUp(self):
        self._test_dice = dice_expression.DiceExpression("4d6")
        self._mock_parser_gen = mock.create_autospec(rply.ParserGenerator)

    def test_dice_add_production_function(self):
        dice_expression.DiceExpression.add_production_function(self._mock_parser_gen)
        self._mock_parser_gen.production.assert_called_once_with(
            """expression : DICE"""
        )

    def test_dice_roll(self):
        self._test_dice = dice_expression.DiceExpression("2d10")
        roll_set = set()
        for _ in range(1000):
            roll_set.add(self._test_dice.roll())
        self.assertEqual(19, len(roll_set))
        self.assertEqual(20, max(roll_set))
        self.assertEqual(2, min(roll_set))

    def test_dice_max(self):
        self.assertEqual(24, self._test_dice.max())

    def test_dice_min(self):
        self.assertEqual(4, self._test_dice.min())

    def test_dice_str(self):
        self.assertEqual("4d6", str(self._test_dice))

    def test_dice_get_probability_distribution(self):
        self._test_dice = dice_expression.DiceExpression("4d6")
        self.assertEqual(
            {
                4: 1,
                5: 4,
                6: 10,
                7: 20,
                8: 35,
                9: 56,
                10: 80,
                11: 104,
                12: 125,
                13: 140,
                14: 146,
                15: 140,
                16: 125,
                17: 104,
                18: 80,
                19: 56,
                20: 35,
                21: 20,
                22: 10,
                23: 4,
                24: 1,
            },
            self._test_dice.get_probability_distribution().get_result_map(),
        )
