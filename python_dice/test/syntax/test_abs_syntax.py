import re
from unittest import TestCase

from python_dice.src.syntax.abs_syntax import AbsSyntax


class TestAbsSyntax(TestCase):
    def test_abs_syntax_get_token_name(self):
        self.assertEqual("ABS", AbsSyntax.get_token_name())

    def test_abs_syntax_get_token_regex(self):
        self.assertEqual(r"\bABS\b", AbsSyntax.get_token_regex())

    def test_abs_syntax_regex_will_match(self):
        test_cases = ["ABS"]
        for test_case in test_cases:
            self.assertTrue(
                re.match(AbsSyntax.get_token_regex(), test_case),
                f"did not match on case test_case {test_case}",
            )

    def test_abs_syntax_regex_will_not_match(self):
        test_cases = ["a", "just a ABSA", "", "1", " ", "-", "+", "(", "!="]
        for test_case in test_cases:
            self.assertIsNone(
                re.match(AbsSyntax.get_token_regex(), test_case),
                f"matched on case test_case {test_case}",
            )
