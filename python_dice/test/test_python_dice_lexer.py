import unittest

import python_dice.src.python_dice_lexer as pydice_lexer


class TestPythonDiceLexer(unittest.TestCase):
    def setUp(self):
        self._test_lexer = pydice_lexer.PythonDiceLexer()

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

    def test_lex_dice(self):
        tokens = self._test_lexer.lex("1d4 * 4d6 + 10d1 - -10000000")

        self.assertEqual(
            ["DICE", "MULTIPLY", "DICE", "ADD", "DICE", "SUBTRACT", "CONSTANT_INTEGER"],
            [token.name for token in tokens],
        )
        self.assertEqual(
            ["1d4", "*", "4d6", "+", "10d1", "-", "-10000000"],
            [token.value for token in tokens],
        )
