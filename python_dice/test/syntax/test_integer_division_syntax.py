import re
from unittest import TestCase

from python_dice.src.syntax.integer_division_syntax import IntegerDivisionSyntax


class TestIntegerDivisionSyntax(TestCase):
    def test_integer_division_get_token_name(self):
        self.assertEqual(
            "INTEGER_DIVISION",
            IntegerDivisionSyntax.get_token_name(),
        )

    def test_integer_division_get_token_regex(self):
        self.assertEqual(r"//", IntegerDivisionSyntax.get_token_regex())

    def test_integer_division_regex_will_match(self):
        test_cases = ["//"]
        for test_case in test_cases:
            self.assertTrue(
                re.match(
                    IntegerDivisionSyntax.get_token_regex(),
                    test_case,
                ),
                "did not match on case test_case %s" % test_case,
            )

    def test_integer_division_regex_will_not_match(self):
        test_cases = ["a", "just a string", "", "1", " ", "-", "+", "(", "/"]
        for test_case in test_cases:
            self.assertIsNone(
                re.match(
                    IntegerDivisionSyntax.get_token_regex(),
                    test_case,
                ),
                "matched on case test_case %s" % test_case,
            )
