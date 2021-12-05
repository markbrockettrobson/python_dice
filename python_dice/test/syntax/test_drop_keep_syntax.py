import re
from unittest import TestCase

from python_dice.src.syntax.drop_keep_syntax import DropKeepSyntax


class TestDropKeepSyntax(TestCase):
    def test_drop_keep_get_token_name(self):
        self.assertEqual("DROP_KEEP_DICE", DropKeepSyntax.get_token_name())

    def test_drop_keep_get_token_regex(self):
        self.assertEqual(
            r"\d*d(\d+|%|F|\[(\s*(-?\d+--?\d+(\*\d+)?|-?\d+(\*\d+)?)\s*,\s*)*\s*(-?\d+--?\d+(\*\d+)?|-?\d+("
            r"\*\d+)?)\s*(,?)\s*\])[kd]\d+",
            DropKeepSyntax.get_token_regex(),
        )

    def test_drop_keep_regex_will_match(self):
        test_cases = [
            "2d6d2",
            "10d4k1",
            "2d30k1",
            "12d90k4",
            "3d210321k314",
            "12652125d12k312",
            "3d%k1",
            "2d%d10",
            "10dFd3",
            "4dFk3",
            "4d[1]k1",
            "4d[-1]d3",
            "10d[ 1,2*4,3*2,4]k3",
            "10d[ 1-4]k3",
            "10d[-4--1*3]k3",
            "2d[-1 , 22, 1, 1]d1",
            "80d[0,1, 2, -1]k10",
            "d[1,]d2",
        ]
        for test_case in test_cases:
            self.assertTrue(
                re.match(DropKeepSyntax.get_token_regex(), test_case),
                f"did not match on case test_case {test_case}",
            )

    def test_drop_keep_regex_will_not_match(self):
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
            "2d2",
            "d210321314",
            "d[1]",
            "d[]k3",
            "d[ 1,,3,4]d6",
            "d[-1 , 2-2, 1, 1]32",
            "10d[-1*-1]d2",
            "10d[--1]d2",
            "10d[-1-]d2",
            "2d[0,1, 2, -1]",
            "5d[1,d3",
        ]
        for test_case in test_cases:
            self.assertIsNone(
                re.match(DropKeepSyntax.get_token_regex(), test_case),
                f"matched on case test_case {test_case}",
            )
