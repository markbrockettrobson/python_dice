import re
from unittest import TestCase

from python_dice.src.syntax.var_syntax import VarSyntax


class TestVarSyntax(TestCase):
    def test_var_syntax_get_token_name(self):
        self.assertEqual("VAR", VarSyntax.get_token_name())

    def test_var_syntax_get_token_regex(self):
        self.assertEqual(r"\bVAR\b", VarSyntax.get_token_regex())

    def test_var_syntax_regex_will_match(self):
        test_cases = ["VAR"]
        for test_case in test_cases:
            self.assertTrue(
                re.match(VarSyntax.get_token_regex(), test_case),
                f"did not match on case test_case {test_case}",
            )

    def test_var_syntax_regex_will_not_match(self):
        test_cases = ["an1", "abbaGold", "var", "1", " ", "-", "+", "(", "!="]
        for test_case in test_cases:
            self.assertIsNone(
                re.match(VarSyntax.get_token_regex(), test_case),
                f"matched on case test_case {test_case}",
            )
