import re
from unittest import TestCase

from python_dice.src.syntax.dice_syntax import DiceSyntax


class TestDiceSyntax(TestCase):
    def test_dice_get_token_name(self):
        self.assertEqual("DICE", DiceSyntax.get_token_name())

    def test_dice_get_token_regex(self):
        self.assertEqual(
            r"\d*d(\d+|%|F|\[(\s*(-?\d+--?\d+(\*\d+)?|-?\d+(\*\d+)?)\s*,\s*)*\s*(-?\d+--?\d+(\*\d+)?|-?\d+("
            r"\*\d+)?)\s*(,?)\s*\])",
            DiceSyntax.get_token_regex(),
        )

    def test_dice_regex_will_match(self):
        test_cases = [
            "2d6",
            "10d4",
            "100d0",
            "1d90",
            "0d210321314",
            "12652125d12312",
            "d6",
            "3d%",
            "d%",
            "dF",
            "10dF",
            "2dF",
            "d[1]",
            "d[-1]",
            "d[ 1,2,3,4]",
            "d[ 1--6,2,3,4*3]",
            "d[-1 , -2--2, 1, 1]",
            "2d[0,1, 2, -1]",
            "2d[0,1, 2*5, -1]",
            "5d[1,]",
        ]
        for test_case in test_cases:
            self.assertTrue(
                re.match(DiceSyntax.get_token_regex(), test_case),
                "did not match on case test_case %s" % test_case,
            )

    def test_dice_regex_will_not_match(self):
        test_cases = [
            "a",
            "just a string",
            "1da",
            "1",
            " ",
            "-",
            "*",
            "(",
            "ad21",
            "5d",
            "5d",
            "5d[]",
            "1d[1, 2, 3",
            "d[1,,2]",
            "-1d[1,2]",
            "1d[1,-2*-2]",
            "1d[1-,2]",
        ]
        for test_case in test_cases:
            self.assertIsNone(
                re.match(DiceSyntax.get_token_regex(), test_case),
                "matched on case test_case %s" % test_case,
            )
