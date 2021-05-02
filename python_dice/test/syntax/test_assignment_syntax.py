import re
import unittest

from python_dice.src.syntax.assignment_syntax import AssignmentSyntax


class TestAssignmentSyntax(unittest.TestCase):
    def test_assignment_get_token_name(self):
        self.assertEqual("ASSIGNMENT", AssignmentSyntax.get_token_name())

    def test_assignment_get_token_regex(self):
        self.assertEqual(r"=(?!=)(?<!==)", AssignmentSyntax.get_token_regex())

    def test_assignment_regex_will_match(self):
        test_cases = ["="]
        for test_case in test_cases:
            self.assertTrue(
                re.match(AssignmentSyntax.get_token_regex(), test_case),
                "did not match on case test_case %s" % test_case,
            )

    def test_assignment_regex_will_not_match(self):
        test_cases = [
            "a",
            "just a string",
            "1d4",
            "1",
            " ",
            "==",
            "*",
            "(",
            "ad21",
            "===s",
        ]
        for test_case in test_cases:
            self.assertIsNone(
                re.match(AssignmentSyntax.get_token_regex(), test_case),
                "matched on case test_case %s" % test_case,
            )
