import re
import unittest

import python_dice.src.python_dice_syntax.abs_syntax as abs_syntax


class TestAbsSyntax(unittest.TestCase):
    def test_abs_syntax_get_token_name(self):
        self.assertEqual("ABS", abs_syntax.AbsSyntax.get_token_name())

    def test_abs_syntax_get_token_regex(self):
        self.assertEqual(r"\bABS\b", abs_syntax.AbsSyntax.get_token_regex())

    def test_abs_syntax_regex_will_match(self):
        test_cases = ["ABS"]
        for test_case in test_cases:
            self.assertTrue(
                re.match(abs_syntax.AbsSyntax.get_token_regex(), test_case),
                "did not match on case test_case %s" % test_case,
            )

    def test_abs_syntax_regex_will_not_match(self):
        test_cases = ["a", "just a ABSA", "", "1", " ", "-", "+", "(", "!="]
        for test_case in test_cases:
            self.assertIsNone(
                re.match(abs_syntax.AbsSyntax.get_token_regex(), test_case),
                "matched on case test_case %s" % test_case,
            )
