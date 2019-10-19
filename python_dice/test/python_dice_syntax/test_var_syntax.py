import re
import unittest

import python_dice.src.python_dice_syntax.var_syntax as var_syntax


class TestVarSyntax(unittest.TestCase):
    def test_var_syntax_get_token_name(self):
        self.assertEqual("VAR", var_syntax.VarSyntax.get_token_name())

    def test_var_syntax_get_token_regex(self):
        self.assertEqual(r"\bVAR\b", var_syntax.VarSyntax.get_token_regex())

    def test_var_syntax_regex_will_match(self):
        test_cases = ["VAR"]
        for test_case in test_cases:
            self.assertTrue(
                re.match(var_syntax.VarSyntax.get_token_regex(), test_case),
                "did not match on case test_case %s" % test_case,
            )

    def test_var_syntax_regex_will_not_match(self):
        test_cases = ["an1", "abbaGold", "var", "1", " ", "-", "+", "(", "!="]
        for test_case in test_cases:
            self.assertIsNone(
                re.match(var_syntax.VarSyntax.get_token_regex(), test_case),
                "matched on case test_case %s" % test_case,
            )
