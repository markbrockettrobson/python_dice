import unittest

import python_dice.src.pydice_parser as pydice_parser


class TestPyDiceLexer(unittest.TestCase):
    def setUp(self):
        self._test_parser = pydice_parser.PyDiceParser()

    def test_lex_constant_integer(self):
        token = self._test_parser.parse("215678284")
        self.assertEqual(
            "CONSTANT_INTEGER", token.get_token_name()
        )  # pylint: disable=maybe-no-member
        self.assertEqual(215678284, token.roll())  # pylint: disable=maybe-no-member
        self.assertEqual(215678284, token.max())  # pylint: disable=maybe-no-member
        self.assertEqual(215678284, token.min())  # pylint: disable=maybe-no-member
