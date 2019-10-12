import re
import unittest
import unittest.mock as mock

import rply

import python_dice.interface.python_dice_syntax.i_dice_statement as i_dice_statement
import python_dice.src.probability_distribution as probability_distribution
import python_dice.src.python_dice_syntax.add as add


class TestAdd(unittest.TestCase):
    def setUp(self):
        self._mock_syntax = [
            mock.create_autospec(i_dice_statement.IDiceSyntax) for _ in range(2)
        ]
        self._mock_syntax[0].roll.return_value = 10
        self._mock_syntax[0].max.return_value = 8
        self._mock_syntax[0].min.return_value = 6
        self._mock_syntax[0].__str__.return_value = "7"
        self._mock_syntax[
            0
        ].get_probability_distribution.return_value = probability_distribution.ProbabilityDistribution(
            {-2: 1, 4: 1}
        )

        self._mock_syntax[1].roll.return_value = 4
        self._mock_syntax[1].max.return_value = 6
        self._mock_syntax[1].min.return_value = 8
        self._mock_syntax[1].__str__.return_value = "2"
        self._mock_syntax[
            1
        ].get_probability_distribution.return_value = probability_distribution.ProbabilityDistribution(
            {8: 1, -3: 2}
        )

        self._test_add = add.Add(self._mock_syntax[0], self._mock_syntax[1])
        self._mock_parser_gen = mock.create_autospec(rply.ParserGenerator)

    def test_add_add_production_function(self):
        add.Add.add_production_function(self._mock_parser_gen)
        self._mock_parser_gen.production.assert_called_once_with(
            """expression : expression ADD expression"""
        )

    def test_add_get_token_name(self):
        self.assertEqual("ADD", self._test_add.get_token_name())
        self.assertEqual("ADD", add.Add.get_token_name())

    def test_add_get_token_regex(self):
        self.assertEqual(r"\+", self._test_add.get_token_regex())
        self.assertEqual(r"\+", add.Add.get_token_regex())

    def test_add_roll(self):
        for _ in range(100):
            self.assertEqual(14, self._test_add.roll())

    def test_add_max(self):
        self.assertEqual(12, self._test_add.max())

    def test_add_min(self):
        self.assertEqual(-5, self._test_add.min())

    def test_add_str(self):
        self.assertEqual("7 + 2", str(self._test_add))

    def test_add_regex_will_match(self):
        test_cases = ["+"]
        for test_case in test_cases:
            self.assertTrue(
                re.match(add.Add.get_token_regex(), test_case),
                "did not match on case test_case %s" % test_case,
            )

    def test_add_regex_will_not_match(self):
        test_cases = ["a", "just a string", "", "1", " ", "-", "*", "("]
        for test_case in test_cases:
            self.assertIsNone(
                re.match(add.Add.get_token_regex(), test_case),
                "matched on case test_case %s" % test_case,
            )

    def test_add_get_probability_distribution(self):
        self._mock_syntax[
            0
        ].get_probability_distribution.return_value = probability_distribution.ProbabilityDistribution(
            {10: 1, -12: 2, 0: 1}
        )
        self._mock_syntax[
            1
        ].get_probability_distribution.return_value = probability_distribution.ProbabilityDistribution(
            {2: 1, 3: 2}
        )
        self.assertEqual(
            {12: 1, -10: 2, 2: 1, 13: 2, -9: 4, 3: 2},
            self._test_add.get_probability_distribution().get_result_map(),
        )
