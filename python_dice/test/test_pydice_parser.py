import unittest
import unittest.mock as mock

import python_dice.src.pydice_lexer as pydice_lexer
import python_dice.src.pydice_parser as pydice_parser


class TestPyDiceParser(unittest.TestCase):
    def setUp(self):
        self._test_parser = pydice_parser.PyDiceParser()
        self._mock_pydice_lexer = mock.create_autospec(pydice_lexer.PyDiceLexer)
        self._mock_token_iter = iter(pydice_lexer.PyDiceLexer().lex("3"))
        self._mock_pydice_lexer.lex.return_value = self._mock_token_iter

    def test_use_injected_lexer(self):
        self._test_parser = pydice_parser.PyDiceParser(self._mock_pydice_lexer)
        self._test_parser.parse("215678284")
        self._mock_pydice_lexer.lex.assert_called_once_with("215678284")

    # pylint: disable=maybe-no-member
    def test_parser_constant_integer(self):
        token = self._test_parser.parse("215678284")
        self.assertEqual("CONSTANT_INTEGER", token.get_token_name())
        self.assertEqual(215678284, token.roll())
        self.assertEqual(215678284, token.max())
        self.assertEqual(215678284, token.min())

    # pylint: disable=maybe-no-member
    def test_parser_add(self):
        token = self._test_parser.parse("3 + -20")
        self.assertEqual("ADD", token.get_token_name())
        self.assertEqual(-17, token.roll())
        self.assertEqual(-17, token.max())
        self.assertEqual(-17, token.min())

    # pylint: disable=maybe-no-member
    def test_parser_subtract(self):
        token = self._test_parser.parse("3 - -20")
        self.assertEqual("SUBTRACT", token.get_token_name())
        self.assertEqual(23, token.roll())
        self.assertEqual(23, token.max())
        self.assertEqual(23, token.min())

    # pylint: disable=maybe-no-member
    def test_parser_add_and_subtract(self):
        token = self._test_parser.parse("3 - -20 + 2")
        self.assertEqual(25, token.roll())
        self.assertEqual(25, token.max())
        self.assertEqual(25, token.min())