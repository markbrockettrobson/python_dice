import re
import unittest

from python_dice.src.syntax.close_parenthesis_syntax import CloseParenthesisSyntax


class TestCloseParenthesisSyntax(unittest.TestCase):
    def test_close_parenthesis_get_token_name(self):
        self.assertEqual(
            "CLOSE_PARENTHESIS",
            CloseParenthesisSyntax.get_token_name(),
        )

    def test_close_parenthesis_get_token_regex(self):
        self.assertEqual(r"\)", CloseParenthesisSyntax.get_token_regex())

    def test_close_parenthesis_regex_will_match(self):
        test_cases = [")"]
        for test_case in test_cases:
            self.assertTrue(
                re.match(
                    CloseParenthesisSyntax.get_token_regex(),
                    test_case,
                ),
                "did not match on case test_case %s" % test_case,
            )

    def testu_close_parenthesis_regex_will_not_match(self):
        test_cases = ["a", "just a string", "", "1", " ", "+", "*", "-", "("]
        for test_case in test_cases:
            self.assertIsNone(
                re.match(
                    CloseParenthesisSyntax.get_token_regex(),
                    test_case,
                ),
                "matched on case test_case %s" % test_case,
            )
