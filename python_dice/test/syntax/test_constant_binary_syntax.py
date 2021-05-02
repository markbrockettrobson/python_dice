import re
from unittest import TestCase

from python_dice.src.syntax.constant_binary_syntax import ConstantBinarySyntax


class TestConstantBinarySyntax(TestCase):
    def test_constant_binary_get_token_name(self):
        self.assertEqual(
            "CONSTANT_BINARY",
            ConstantBinarySyntax.get_token_name(),
        )

    def test_constant_binary_get_token_regex(self):
        self.assertEqual(
            r"\bTrue\b|\bFalse\b",
            ConstantBinarySyntax.get_token_regex(),
        )

    def test_constant_binary_regex_will_match(self):
        test_cases = ["True", "False"]
        for test_case in test_cases:
            self.assertTrue(
                re.match(
                    ConstantBinarySyntax.get_token_regex(),
                    test_case,
                ),
                "did not match on case test_case %s" % test_case,
            )

    def test_constant_binary_regex_will_not_match(self):
        test_cases = [
            "a",
            "just a string",
            "1",
            "0",
            "!",
            "false",
            "Falses",
            "aTrue",
            "true",
        ]
        for test_case in test_cases:
            self.assertIsNone(
                re.match(
                    ConstantBinarySyntax.get_token_regex(),
                    test_case,
                ),
                "matched on case test_case %s" % test_case,
            )
