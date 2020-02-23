import unittest
import unittest.mock as mock

import rply

import python_dice.src.python_dice_expression.drop_keep_expression as drop_keep_expression


class TestDiceExpression(unittest.TestCase):
    def setUp(self):
        self._test_dice_drop = drop_keep_expression.DropKeepExpression("4d6d2")
        self._test_dice_keep = drop_keep_expression.DropKeepExpression("4d6k2")
        self._mock_parser_gen = mock.create_autospec(rply.ParserGenerator)

    def test_drop_keep_add_production_function(self):
        drop_keep_expression.DropKeepExpression.add_production_function(self._mock_parser_gen)
        self._mock_parser_gen.production.assert_called_once_with(
            """expression : DROP_KEEP_DICE"""
        )

    def test_drop_keep_roll_keep(self):
        test_dice = drop_keep_expression.DropKeepExpression("5d10k2")
        roll_set_drop = set()
        for _ in range(10000):
            roll_set_drop.add(test_dice.roll())
        self.assertEqual(20, max(roll_set_drop))

    def test_drop_keep_roll_drop(self):
        test_dice = drop_keep_expression.DropKeepExpression("5d10d3")
        roll_set_keep = set()
        for _ in range(10000):
            roll_set_keep.add(test_dice.roll())
        self.assertEqual(2, min(roll_set_keep))

    def test_drop_keep_max_drop(self):
        self.assertEqual(12, self._test_dice_drop.max())

    def test_drop_keep_max_keep(self):
        self.assertEqual(12, self._test_dice_keep.max())

    def test_drop_keep_min_drop(self):
        self.assertEqual(2, self._test_dice_drop.min())

    def test_drop_keep_min_keep(self):
        self.assertEqual(2, self._test_dice_keep.min())

    def test_drop_keep_str_drop(self):
        self.assertEqual("4d6d2", str(self._test_dice_drop))

    def test_drop_keep_str_keep(self):
        self.assertEqual("4d6k2", str(self._test_dice_keep))

    def test_drop_keep_get_probability_distribution_drop(self):
        test_dice = drop_keep_expression.DropKeepExpression("6d4d4")
        self.assertEqual(
            {
                2: 1909,
                3: 1266,
                4: 659,
                5: 192,
                6: 63,
                7: 6,
                8: 1,
            },
            test_dice.get_probability_distribution().get_result_map(),
        )

    def test_drop_keep_get_probability_distribution_drop_large_dice(self):
        test_dice = drop_keep_expression.DropKeepExpression("6d8d4")
        self.assertEqual(
            {
                2: 43653,
                3: 54186,
                4: 52243,
                5: 40512,
                6: 29573,
                7: 18558,
                8: 11523,
                9: 6144,
                10: 3367,
                11: 1458,
                12: 665,
                13: 192,
                14: 63,
                15: 6,
                16: 1,
            },
            test_dice.get_probability_distribution().get_result_map(),
        )

    def test_drop_keep_get_probability_distribution_drop_large_number_dice(self):
        test_dice = drop_keep_expression.DropKeepExpression("20d3d16")
        self.assertEqual(
            {
                4: 3276020625,
                5: 149420940,
                6: 49804890,
                7: 10485360,
                8: 1050835,
                9: 1520,
                10: 210,
                11: 20,
                12: 1,
            },
            test_dice.get_probability_distribution().get_result_map(),
        )

    def test_drop_keep_get_probability_distribution_keep(self):
        test_dice = drop_keep_expression.DropKeepExpression("6d4k2")
        self.assertEqual(
            {
                2: 1,
                3: 6,
                4: 63,
                5: 192,
                6: 659,
                7: 1266,
                8: 1909,
            },
            test_dice.get_probability_distribution().get_result_map(),
        )

    def test_drop_keep_get_probability_distribution_keep_large_dice(self):
        test_dice = drop_keep_expression.DropKeepExpression("6d8k2")
        self.assertEqual(
            {
                2: 1,
                3: 6,
                4: 63,
                5: 192,
                6: 665,
                7: 1458,
                8: 3367,
                9: 6144,
                10: 11523,
                11: 18558,
                12: 29573,
                13: 40512,
                14: 52243,
                15: 54186,
                16: 43653,
            },
            test_dice.get_probability_distribution().get_result_map(),
        )

    def test_drop_keep_get_probability_distribution_keep_large_number_dice(self):
        test_dice = drop_keep_expression.DropKeepExpression("20d3k4")
        self.assertEqual(
            {
                4: 1,
                5: 20,
                6: 210,
                7: 1520,
                8: 1050835,
                9: 10485360,
                10: 49804890,
                11: 149420940,
                12: 3276020625,
            },
            test_dice.get_probability_distribution().get_result_map(),
        )

    def test_drop_keep_get_probability_distribution_keep_to_many(self):
        test_dice = drop_keep_expression.DropKeepExpression("2d3k10")
        self.assertEqual(
            {
                2: 1,
                3: 2,
                4: 3,
                5: 2,
                6: 1,
            },
            test_dice.get_probability_distribution().get_result_map(),
        )

    def test_drop_keep_get_probability_distribution_drop_to_many(self):
        test_dice = drop_keep_expression.DropKeepExpression("2d3d10")
        self.assertEqual(
            {
                0: 1,
            },
            test_dice.get_probability_distribution().get_result_map(),
        )

    def test_drop_keep_get_probability_distribution_keep_to_zero(self):
        test_dice = drop_keep_expression.DropKeepExpression("2d3k0")
        self.assertEqual(
            {
                0: 1,
            },
            test_dice.get_probability_distribution().get_result_map(),
        )

    def test_drop_keep_get_probability_distribution_drop_to_zero(self):
        test_dice = drop_keep_expression.DropKeepExpression("2d3d0")
        self.assertEqual(
            {
                2: 1,
                3: 2,
                4: 3,
                5: 2,
                6: 1,
            },
            test_dice.get_probability_distribution().get_result_map(),
        )
