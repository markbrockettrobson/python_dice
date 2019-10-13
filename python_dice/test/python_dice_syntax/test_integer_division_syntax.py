import re
import unittest

import python_dice.src.python_dice_syntax.integer_division_syntax as integer_division_syntax


class TestIntegerDivisionSyntax(unittest.TestCase):
    def test_integer_division_get_token_name(self):
        self.assertEqual(
            "INTEGER_DIVISION",
            integer_division_syntax.IntegerDivisionSyntax.get_token_name(),
        )

    def test_integer_division_get_token_regex(self):
        self.assertEqual(
            r"//", integer_division_syntax.IntegerDivisionSyntax.get_token_regex()
        )

    def test_integer_division_regex_will_match(self):
        test_cases = ["//"]
        for test_case in test_cases:
            self.assertTrue(
                re.match(
                    integer_division_syntax.IntegerDivisionSyntax.get_token_regex(),
                    test_case,
                ),
                "did not match on case test_case %s" % test_case,
            )

    def test_integer_division_regex_will_not_match(self):
        test_cases = ["a", "just a string", "", "1", " ", "-", "+", "(", "/"]
        for test_case in test_cases:
            self.assertIsNone(
                re.match(
                    integer_division_syntax.IntegerDivisionSyntax.get_token_regex(),
                    test_case,
                ),
                "matched on case test_case %s" % test_case,
            )
