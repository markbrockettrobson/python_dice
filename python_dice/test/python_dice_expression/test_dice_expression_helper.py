import unittest

import python_dice.src.python_dice_expression.dice_expression_helper as dice_expression_helper


class TestDiceExpressionHelper(unittest.TestCase):
    def test_numbered_dice(self):
        self.assertEqual(
            {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 1},
            dice_expression_helper.get_single_dice_outcome_map("6"),
        )

    def test_fate_dice(self):
        self.assertEqual(
            {-1: 1, 0: 1, 1: 1}, dice_expression_helper.get_single_dice_outcome_map("F")
        )

    def test_percentile_dice(self):
        self.assertEqual(
            {i: 1 for i in range(1, 101)},
            dice_expression_helper.get_single_dice_outcome_map("%"),
        )

    def test_custom_dice(self):
        self.assertEqual(
            {2: 1, -9: 1, 1: 1},
            dice_expression_helper.get_single_dice_outcome_map("[2, -9, 1]"),
        )

    def test_custom_dice_repeated_sides(self):
        self.assertEqual(
            {2: 2, -9: 1, 1: 5},
            dice_expression_helper.get_single_dice_outcome_map(
                "[2, -9, 1, 1, 1, 1, 1 ,2     ]"
            ),
        )

    def test_custom_dice_range(self):
        self.assertEqual(
            {7: 1, 8: 1, 9: 1},
            dice_expression_helper.get_single_dice_outcome_map("[7-9]"),
        )

    def test_custom_dice_range_negative(self):
        self.assertEqual(
            {-3: 1, -2: 1, -1: 1, 0: 1, 1: 1, 2: 1},
            dice_expression_helper.get_single_dice_outcome_map("[-3-2]"),
        )

    def test_custom_dice_range_negative_to_negative(self):
        self.assertEqual(
            {-10: 1, -9: 1, -8: 1, -7: 1, -3: 1, -2: 1, -1: 1, 0: 1},
            dice_expression_helper.get_single_dice_outcome_map("[-3--1, -10--7, 0]"),
        )

    def test_custom_dice_range_out_of_order_range(self):
        self.assertEqual(
            {-3: 1, -2: 1, -1: 1, 1: 1, 2: 1, 3: 1, 4: 1},
            dice_expression_helper.get_single_dice_outcome_map("[4-1, -1--3]"),
        )

    def test_custom_dice_multiplier(self):
        self.assertEqual(
            {5: 79, 4: 1},
            dice_expression_helper.get_single_dice_outcome_map("[4*1, 5*79]"),
        )

    def test_custom_dice_multiplier_range(self):
        self.assertEqual(
            {-1: 10, 0: 10, 1: 10, 4: 2, 5: 2, 6: 2, 7: 2, 8: 2},
            dice_expression_helper.get_single_dice_outcome_map("[4-8*2, -1-1*10]"),
        )
