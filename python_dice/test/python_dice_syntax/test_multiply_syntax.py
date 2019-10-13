import re
import unittest

import python_dice.src.python_dice_syntax.multiply_syntax as multiply_syntax


class TestMultiplySyntax(unittest.TestCase):
    def test_multiply_get_token_name(self):
        self.assertEqual("MULTIPLY", multiply_syntax.MultiplySyntax.get_token_name())

    def test_multiply_get_token_regex(self):
        self.assertEqual(r"\*", multiply_syntax.MultiplySyntax.get_token_regex())

    def test_multiply_regex_will_match(self):
        test_cases = ["*"]
        for test_case in test_cases:
            self.assertTrue(
                re.match(multiply_syntax.MultiplySyntax.get_token_regex(), test_case),
                "did not match on case test_case %s" % test_case,
            )

    def test_multiply_regex_will_not_match(self):
        test_cases = ["a", "just a string", "", "1", " ", "-", "+", "("]
        for test_case in test_cases:
            self.assertIsNone(
                re.match(multiply_syntax.MultiplySyntax.get_token_regex(), test_case),
                "matched on case test_case %s" % test_case,
            )
