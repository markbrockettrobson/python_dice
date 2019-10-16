import re
import unittest

import python_dice.src.python_dice_syntax.min_max_syntax as min_max_syntax


class TestMinMaxSyntax(unittest.TestCase):
    def test_min_max_get_token_name(self):
        self.assertEqual("MINMAX", min_max_syntax.MinMaxSyntax.get_token_name())

    def test_min_max_get_token_regex(self):
        self.assertEqual(
            r"\bMAX\b|\bMIN\b", min_max_syntax.MinMaxSyntax.get_token_regex()
        )

    def test_min_max_regex_will_match(self):
        test_cases = ["MAX", "MIN"]
        for test_case in test_cases:
            self.assertTrue(
                re.match(min_max_syntax.MinMaxSyntax.get_token_regex(), test_case),
                "did not match on case test_case %s" % test_case,
            )

    def test_min_max_regex_will_not_match(self):
        test_cases = [
            "a",
            "just a string",
            "1d4",
            "1",
            " ",
            "-",
            "*",
            "(",
            "ad21",
            "MAXAMA",
            "AMIN",
            "max",
            "min",
        ]
        for test_case in test_cases:
            self.assertIsNone(
                re.match(min_max_syntax.MinMaxSyntax.get_token_regex(), test_case),
                "matched on case test_case %s" % test_case,
            )
