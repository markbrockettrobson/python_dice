import re
import unittest

import python_dice.src.python_dice_syntax.constant_binary_syntax as constant_binary_syntax


class TestConstantBinarySyntax(unittest.TestCase):
    def test_constant_binary_get_token_name(self):
        self.assertEqual(
            "CONSTANT_BINARY",
            constant_binary_syntax.ConstantBinarySyntax.get_token_name(),
        )

    def test_constant_binary_get_token_regex(self):
        self.assertEqual(
            r"\bTrue\b|\bFalse\b",
            constant_binary_syntax.ConstantBinarySyntax.get_token_regex(),
        )

    def test_constant_binary_regex_will_match(self):
        test_cases = ["True", "False"]
        for test_case in test_cases:
            self.assertTrue(
                re.match(
                    constant_binary_syntax.ConstantBinarySyntax.get_token_regex(),
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
                    constant_binary_syntax.ConstantBinarySyntax.get_token_regex(),
                    test_case,
                ),
                "matched on case test_case %s" % test_case,
            )
