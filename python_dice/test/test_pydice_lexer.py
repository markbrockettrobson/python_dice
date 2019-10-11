import unittest

import python_dice.src.pydice_lexer as pydice_lexer


class TestPyDiceLexer(unittest.TestCase):
    def setUp(self):
        self._test_lexer = pydice_lexer.PyDiceLexer()

    def test_lex_constant_integer(self):
        tokens = self._test_lexer.lex("1 3 4 5 -10 0 -10000000")
        for token in tokens:
            self.assertEqual("CONSTANT_INTEGER", token.name)
        self.assertEqual(
            ["1", "3", "4", "5", "-10", "0", "-10000000"],
            [token.value for token in tokens],
        )

    def test_lex_add(self):
        tokens = self._test_lexer.lex("1 + 4 + -10 + -10000000")

        self.assertEqual(
            [
                "CONSTANT_INTEGER",
                "ADD",
                "CONSTANT_INTEGER",
                "ADD",
                "CONSTANT_INTEGER",
                "ADD",
                "CONSTANT_INTEGER",
            ],
            [token.name for token in tokens],
        )
        self.assertEqual(
            ["1", "+", "4", "+", "-10", "+", "-10000000"],
            [token.value for token in tokens],
        )

    def test_lex_subtract(self):
        tokens = self._test_lexer.lex("1 - 4 - -10 - -10000000")

        self.assertEqual(
            [
                "CONSTANT_INTEGER",
                "SUBTRACT",
                "CONSTANT_INTEGER",
                "SUBTRACT",
                "CONSTANT_INTEGER",
                "SUBTRACT",
                "CONSTANT_INTEGER",
            ],
            [token.name for token in tokens],
        )
        self.assertEqual(
            ["1", "-", "4", "-", "-10", "-", "-10000000"],
            [token.value for token in tokens],
        )

    def test_lex_multiply(self):
        tokens = self._test_lexer.lex("1 * 4 * -10 * -10000000")

        self.assertEqual(
            [
                "CONSTANT_INTEGER",
                "MULTIPLY",
                "CONSTANT_INTEGER",
                "MULTIPLY",
                "CONSTANT_INTEGER",
                "MULTIPLY",
                "CONSTANT_INTEGER",
            ],
            [token.name for token in tokens],
        )
        self.assertEqual(
            ["1", "*", "4", "*", "-10", "*", "-10000000"],
            [token.value for token in tokens],
        )
