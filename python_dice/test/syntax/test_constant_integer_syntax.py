import re
import unittest

from python_dice.src.syntax.constant_integer_syntax import ConstantIntegerSyntax


class TestConstantIntegerSyntax(unittest.TestCase):
    def test_constant_integers_get_token_name(self):
        self.assertEqual(
            "CONSTANT_INTEGER",
            ConstantIntegerSyntax.get_token_name(),
        )

    def test_constant_integers_get_token_regex(self):
        self.assertEqual(r"-?\d+", ConstantIntegerSyntax.get_token_regex())

    def test_constant_integer_regex_will_match(self):
        test_cases = [
            "-31982473918274",
            "-3",
            "0",
            "1",
            "0003",
            "12",
            "41",
            "87",
            "902",
            "12983",
            "15412",
            "1000000000000000000000000000",
        ]
        for test_case in test_cases:
            self.assertTrue(
                re.match(
                    ConstantIntegerSyntax.get_token_regex(),
                    test_case,
                ),
                "did not match on case test_case %s" % test_case,
            )

    def test_constant_integer_regex_will_not_match(self):
        test_cases = ["a", "just a string", "", " "]
        for test_case in test_cases:
            self.assertIsNone(
                re.match(
                    ConstantIntegerSyntax.get_token_regex(),
                    test_case,
                ),
                "matched on case test_case %s" % test_case,
            )
