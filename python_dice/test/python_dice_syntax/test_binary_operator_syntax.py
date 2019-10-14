import re
import unittest

import python_dice.src.python_dice_syntax.binary_operator_syntax as binary_operator_syntax


class TestBinaryOperatorSyntax(unittest.TestCase):
    def test_binary_operator_syntax_get_token_name(self):
        self.assertEqual(
            "BINARY_OPERATOR",
            binary_operator_syntax.BinaryOperatorSyntax.get_token_name(),
        )

    def test_binary_operator_syntax_get_token_regex(self):
        self.assertEqual(
            r"==|!=|<=|<|>=|>|\bAND\b|\bOR\b",
            binary_operator_syntax.BinaryOperatorSyntax.get_token_regex(),
        )

    def test_binary_operator_syntax_regex_will_match(self):
        test_cases = ["==", "!=", "<", "<=", ">", ">=", "AND", "OR"]
        for test_case in test_cases:
            self.assertTrue(
                re.match(
                    binary_operator_syntax.BinaryOperatorSyntax.get_token_regex(),
                    test_case,
                ),
                "did not match on case test_case %s" % test_case,
            )

    def test_binary_operator_syntax_regex_will_not_match(self):
        test_cases = ["a", "just a string", "", "1", " ", "-", "+", "(", "!"]
        for test_case in test_cases:
            self.assertIsNone(
                re.match(
                    binary_operator_syntax.BinaryOperatorSyntax.get_token_regex(),
                    test_case,
                ),
                "matched on case test_case %s" % test_case,
            )
