import re
import unittest

import python_dice.src.python_dice_syntax.comma_syntax as comma_syntax


class TestCommaSyntax(unittest.TestCase):
    def test_comma_get_token_name(self):
        self.assertEqual("COMMA", comma_syntax.CommaSyntax.get_token_name())

    def test_comma_get_token_regex(self):
        self.assertEqual(r"\,", comma_syntax.CommaSyntax.get_token_regex())

    def test_comma_regex_will_match(self):
        test_cases = [","]
        for test_case in test_cases:
            self.assertTrue(
                re.match(comma_syntax.CommaSyntax.get_token_regex(), test_case),
                "did not match on case test_case %s" % test_case,
            )

    def test_comma_regex_will_not_match(self):
        test_cases = ["a", "just a string", "1d4", "1", " ", "-", "*", "(", "ad21"]
        for test_case in test_cases:
            self.assertIsNone(
                re.match(comma_syntax.CommaSyntax.get_token_regex(), test_case),
                "matched on case test_case %s" % test_case,
            )
