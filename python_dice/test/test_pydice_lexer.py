import unittest

import python_dice.src.pydice_lexer as pydice_lexer


class TestPyDiceLexer(unittest.TestCase):
    def setUp(self):
        self._test_lexer = pydice_lexer.PyDiceLexer()

    def test_lex_constant_integer(self):
        tokens = self._test_lexer.lex(" 1 3 4 5 -10 0 -10000000")
        for token in tokens:
            self.assertEqual("CONSTANT_INTEGER", token.name)
        self.assertEqual(
            ["1", "3", "4", "5", "-10", "0", "-10000000"],
            [token.value for token in tokens],
        )
