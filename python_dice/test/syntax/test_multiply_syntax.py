import re
from unittest import TestCase

from python_dice.src.syntax.multiply_syntax import MultiplySyntax


class TestMultiplySyntax(TestCase):
    def test_multiply_get_token_name(self):
        self.assertEqual("MULTIPLY", MultiplySyntax.get_token_name())

    def test_multiply_get_token_regex(self):
        self.assertEqual(r"\*", MultiplySyntax.get_token_regex())

    def test_multiply_regex_will_match(self):
        test_cases = ["*"]
        for test_case in test_cases:
            self.assertTrue(
                re.match(MultiplySyntax.get_token_regex(), test_case),
                "did not match on case test_case %s" % test_case,
            )

    def test_multiply_regex_will_not_match(self):
        test_cases = ["a", "just a string", "", "1", " ", "-", "+", "("]
        for test_case in test_cases:
            self.assertIsNone(
                re.match(MultiplySyntax.get_token_regex(), test_case),
                "matched on case test_case %s" % test_case,
            )
