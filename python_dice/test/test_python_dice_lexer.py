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

    def test_lex_parenthesis(self):
        tokens = self._test_lexer.lex("((1d4 * 4d6) + 10d1) - -10000000")

        self.assertEqual(
            [
                "OPEN_PARENTHESIS",
                "OPEN_PARENTHESIS",
                "DICE",
                "MULTIPLY",
                "DICE",
                "CLOSE_PARENTHESIS",
                "ADD",
                "DICE",
                "CLOSE_PARENTHESIS",
                "SUBTRACT",
                "CONSTANT_INTEGER",
            ],
            [token.name for token in tokens],
        )
        self.assertEqual(
            ["(", "(", "1d4", "*", "4d6", ")", "+", "10d1", ")", "-", "-10000000"],
            [token.value for token in tokens],
        )

    def test_lex_constant_binary(self):
        tokens = self._test_lexer.lex("((1d4 * True) + 10d1) - False")

        self.assertEqual(
            [
                "OPEN_PARENTHESIS",
                "OPEN_PARENTHESIS",
                "DICE",
                "MULTIPLY",
                "CONSTANT_BINARY",
                "CLOSE_PARENTHESIS",
                "ADD",
                "DICE",
                "CLOSE_PARENTHESIS",
                "SUBTRACT",
                "CONSTANT_BINARY",
            ],
            [token.name for token in tokens],
        )
        self.assertEqual(
            ["(", "(", "1d4", "*", "True", ")", "+", "10d1", ")", "-", "False"],
            [token.value for token in tokens],
        )

    def test_lex_not(self):
        tokens = self._test_lexer.lex("!(!1d4 + True)")

        self.assertEqual(
            [
                "NOT",
                "OPEN_PARENTHESIS",
                "NOT",
                "DICE",
                "ADD",
                "CONSTANT_BINARY",
                "CLOSE_PARENTHESIS",
            ],
            [token.name for token in tokens],
        )
        self.assertEqual(
            ["!", "(", "!", "1d4", "+", "True", ")"], [token.value for token in tokens]
        )

    def test_lex_equals(self):
        tokens = self._test_lexer.lex("1d4 == True")

        self.assertEqual(
            ["DICE", "BINARY_OPERATOR", "CONSTANT_BINARY"],
            [token.name for token in tokens],
        )
        self.assertEqual(["1d4", "==", "True"], [token.value for token in tokens])

    def test_lex_not_equals(self):
        tokens = self._test_lexer.lex("1d4 != True")

        self.assertEqual(
            ["DICE", "BINARY_OPERATOR", "CONSTANT_BINARY"],
            [token.name for token in tokens],
        )
        self.assertEqual(["1d4", "!=", "True"], [token.value for token in tokens])

    def test_lex_less_than(self):
        tokens = self._test_lexer.lex("1d4 < True <= 1d3")

        self.assertEqual(
            ["DICE", "BINARY_OPERATOR", "CONSTANT_BINARY", "BINARY_OPERATOR", "DICE"],
            [token.name for token in tokens],
        )
        self.assertEqual(
            ["1d4", "<", "True", "<=", "1d3"], [token.value for token in tokens]
        )

    def test_lex_greater_than(self):
        tokens = self._test_lexer.lex("1d4 > True >= 1d3")

        self.assertEqual(
            ["DICE", "BINARY_OPERATOR", "CONSTANT_BINARY", "BINARY_OPERATOR", "DICE"],
            [token.name for token in tokens],
        )
        self.assertEqual(
            ["1d4", ">", "True", ">=", "1d3"], [token.value for token in tokens]
        )

    def test_lex_and(self):
        tokens = self._test_lexer.lex("1d4 AND True")

        self.assertEqual(
            ["DICE", "BINARY_OPERATOR", "CONSTANT_BINARY"],
            [token.name for token in tokens],
        )
        self.assertEqual(["1d4", "AND", "True"], [token.value for token in tokens])

    def test_lex_or(self):
        tokens = self._test_lexer.lex("1d4 OR True")

        self.assertEqual(
            ["DICE", "BINARY_OPERATOR", "CONSTANT_BINARY"],
            [token.name for token in tokens],
        )
        self.assertEqual(["1d4", "OR", "True"], [token.value for token in tokens])

    def test_lex_max(self):
        tokens = self._test_lexer.lex("MAX(1d4, 3)")

        self.assertEqual(
            [
                "MINMAX",
                "OPEN_PARENTHESIS",
                "DICE",
                "COMMA",
                "CONSTANT_INTEGER",
                "CLOSE_PARENTHESIS",
            ],
            [token.name for token in tokens],
        )
        self.assertEqual(
            ["MAX", "(", "1d4", ",", "3", ")"], [token.value for token in tokens]
        )

    def test_lex_min(self):
        tokens = self._test_lexer.lex("MIN(4, 1d6)")

        self.assertEqual(
            [
                "MINMAX",
                "OPEN_PARENTHESIS",
                "CONSTANT_INTEGER",
                "COMMA",
                "DICE",
                "CLOSE_PARENTHESIS",
            ],
            [token.name for token in tokens],
        )
        self.assertEqual(
            ["MIN", "(", "4", ",", "1d6", ")"], [token.value for token in tokens]
        )
