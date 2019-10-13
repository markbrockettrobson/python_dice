import re
import unittest

import python_dice.src.python_dice_syntax.subtract_syntax as subtract_syntax


class TestSubtractSyntax(unittest.TestCase):
    def test_subtract_get_token_name(self):
        self.assertEqual("SUBTRACT", subtract_syntax.SubtractSyntax.get_token_name())

    def test_subtract_get_token_regex(self):
        self.assertEqual(r"\-", subtract_syntax.SubtractSyntax.get_token_regex())

    def test_subtract_regex_will_match(self):
        test_cases = ["-"]
        for test_case in test_cases:
            self.assertTrue(
                re.match(subtract_syntax.SubtractSyntax.get_token_regex(), test_case),
                "did not match on case test_case %s" % test_case,
            )

    def test_subtract_regex_will_not_match(self):
        test_cases = ["a", "just a string", "", "1", " ", "+", "*", "("]
        for test_case in test_cases:
            self.assertIsNone(
                re.match(subtract_syntax.SubtractSyntax.get_token_regex(), test_case),
                "matched on case test_case %s" % test_case,
            )
