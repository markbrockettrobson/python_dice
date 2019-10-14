import re
import unittest

import python_dice.src.python_dice_syntax.not_syntax as not_syntax


class TestNotSyntax(unittest.TestCase):
    def test_not_syntax_get_token_name(self):
        self.assertEqual("NOT", not_syntax.NotSyntax.get_token_name())

    def test_not_syntax_get_token_regex(self):
        self.assertEqual(r"!(?!=)", not_syntax.NotSyntax.get_token_regex())

    def test_not_syntax_regex_will_match(self):
        test_cases = ["!"]
        for test_case in test_cases:
            self.assertTrue(
                re.match(not_syntax.NotSyntax.get_token_regex(), test_case),
                "did not match on case test_case %s" % test_case,
            )

    def test_not_syntax_regex_will_not_match(self):
        test_cases = ["a", "just a string", "", "1", " ", "-", "+", "(", "!="]
        for test_case in test_cases:
            self.assertIsNone(
                re.match(not_syntax.NotSyntax.get_token_regex(), test_case),
                "matched on case test_case %s" % test_case,
            )
