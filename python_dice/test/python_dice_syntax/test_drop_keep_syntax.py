import re
import unittest

import python_dice.src.python_dice_syntax.drop_keep_syntax as drop_keep_syntax


class TestDropKeepSyntax(unittest.TestCase):
    def test_drop_keep_get_token_name(self):
        self.assertEqual(
            "DROP_KEEP_DICE", drop_keep_syntax.DropKeepSyntax.get_token_name()
        )

    def test_drop_keep_get_token_regex(self):
        self.assertEqual(
            r"\d+d\d+[kdKD]\d+", drop_keep_syntax.DropKeepSyntax.get_token_regex()
        )

    def test_drop_keep_regex_will_match(self):
        test_cases = [
            "2d6d2",
            "10d4k1",
            "2d30k1",
            "12d90k4",
            "3d210321k314",
            "12652125d12k312",
        ]
        for test_case in test_cases:
            self.assertTrue(
                re.match(drop_keep_syntax.DropKeepSyntax.get_token_regex(), test_case),
                "did not match on case test_case %s" % test_case,
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
        ]
        for test_case in test_cases:
            self.assertIsNone(
                re.match(drop_keep_syntax.DropKeepSyntax.get_token_regex(), test_case),
                "matched on case test_case %s" % test_case,
            )
