import re
from unittest import TestCase

from python_dice.src.syntax.not_syntax import NotSyntax


class TestNotSyntax(TestCase):
    def test_not_syntax_get_token_name(self):
        self.assertEqual("NOT", NotSyntax.get_token_name())

    def test_not_syntax_get_token_regex(self):
        self.assertEqual(r"!(?!=)", NotSyntax.get_token_regex())

    def test_not_syntax_regex_will_match(self):
        test_cases = ["!"]
        for test_case in test_cases:
            self.assertTrue(
                re.match(NotSyntax.get_token_regex(), test_case),
                f"did not match on case test_case {test_case}",
            )

    def test_not_syntax_regex_will_not_match(self):
        test_cases = ["a", "just a string", "", "1", " ", "-", "+", "(", "!="]
        for test_case in test_cases:
            self.assertIsNone(
                re.match(NotSyntax.get_token_regex(), test_case),
                f"matched on case test_case {test_case}",
            )
