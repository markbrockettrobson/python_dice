import re
import unittest

from python_dice.src.syntax.name_syntax import NameSyntax


class TestNameSyntax(unittest.TestCase):
    def test_name_syntax_get_token_name(self):
        self.assertEqual("NAME", NameSyntax.get_token_name())

    def test_name_syntax_get_token_regex(self):
        self.assertEqual(r"\b[a-z_]+\b", NameSyntax.get_token_regex())

    def test_name_syntax_regex_will_match(self):
        test_cases = ["apple", "hi", "i", "abcdefghijklmnopqrstuvwxyz", "two_words"]
        for test_case in test_cases:
            self.assertTrue(
                re.match(NameSyntax.get_token_regex(), test_case),
                "did not match on case test_case %s" % test_case,
            )

    def test_name_syntax_regex_will_not_match(self):
        test_cases = ["an1", "abbaGold", "", "1", " ", "-", "+", "(", "!="]
        for test_case in test_cases:
            self.assertIsNone(
                re.match(NameSyntax.get_token_regex(), test_case),
                "matched on case test_case %s" % test_case,
            )
