import re
import unittest
import unittest.mock as mock

import rply

import python_dice.src.pydice_syntax.constant_integer as constant_integer


class TestConstantInteger(unittest.TestCase):
    def setUp(self):
        self._test_constant_integers = constant_integer.ConstantInteger("14")
        self._mock_parser_gen = mock.create_autospec(rply.ParserGenerator)

    def test_constant_integers_add_production_function(self):
        constant_integer.ConstantInteger.add_production_function(self._mock_parser_gen)
        self._mock_parser_gen.production.assert_called_once_with(
            """expression : CONSTANT_INTEGER"""
        )

    def test_constant_integers_get_token_name(self):
        self.assertEqual(
            "CONSTANT_INTEGER", self._test_constant_integers.get_token_name()
        )
        self.assertEqual(
            "CONSTANT_INTEGER", constant_integer.ConstantInteger.get_token_name()
        )

    def test_constant_integers_get_token_regex(self):
        self.assertEqual(r"-?\d+", self._test_constant_integers.get_token_regex())
        self.assertEqual(r"-?\d+", constant_integer.ConstantInteger.get_token_regex())

    def test_constant_integers_roll(self):
        for _ in range(100):
            self.assertEqual(14, self._test_constant_integers.roll())

    def test_constant_integers_max(self):
        self.assertEqual(14, self._test_constant_integers.max())

    def test_constant_integers_min(self):
        self.assertEqual(14, self._test_constant_integers.min())

    def test_constant_integers_str(self):
        self.assertEqual("14", str(self._test_constant_integers))

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
                re.match(constant_integer.ConstantInteger.get_token_regex(), test_case),
                "did not match on case test_case %s" % test_case,
            )

    def test_constant_integer_regex_will_not_match(self):
        test_cases = ["a", "just a string", "", " "]
        for test_case in test_cases:
            self.assertIsNone(
                re.match(constant_integer.ConstantInteger.get_token_regex(), test_case),
                "matched on case test_case %s" % test_case,
            )
