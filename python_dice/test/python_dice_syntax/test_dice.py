import re
import unittest
import unittest.mock as mock

import rply

import python_dice.interface.python_dice_syntax.i_dice_statement as i_dice_statement
import python_dice.src.probability_distribution as probability_distribution
import python_dice.src.python_dice_syntax.dice as dice


class TestDice(unittest.TestCase):
    def setUp(self):
        self._test_dice = dice.Dice("4d6")
        self._mock_parser_gen = mock.create_autospec(rply.ParserGenerator)

    def test_dice_add_production_function(self):
        dice.Dice.add_production_function(self._mock_parser_gen)
        self._mock_parser_gen.production.assert_called_once_with(
            """expression : DICE"""
        )

    def test_dice_get_token_name(self):
        self.assertEqual("DICE", self._test_dice.get_token_name())
        self.assertEqual("DICE", dice.Dice.get_token_name())

    def test_dice_get_token_regex(self):
        self.assertEqual(r"\d+d\d+", self._test_dice.get_token_regex())
        self.assertEqual(r"\d+d\d+", dice.Dice.get_token_regex())

    def test_dice_roll(self):
        self._test_dice = dice.Dice("2d10")
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

    def test_dice_regex_will_match(self):
        test_cases = ["2d6", "10d4", "100d0", "1d90", "0d210321314", "12652125d12312"]
        for test_case in test_cases:
            self.assertTrue(
                re.match(dice.Dice.get_token_regex(), test_case),
                "did not match on case test_case %s" % test_case,
            )

    def test_dice_regex_will_not_match(self):
        test_cases = ["a", "just a string", "1da", "1", " ", "-", "*", "(", "ad21"]
        for test_case in test_cases:
            self.assertIsNone(
                re.match(dice.Dice.get_token_regex(), test_case),
                "matched on case test_case %s" % test_case,
            )

    def test_dice_get_probability_distribution(self):
        self._test_dice = dice.Dice("4d6")
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
