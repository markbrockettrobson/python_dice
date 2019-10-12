import unittest

import python_dice.src.probability_distribution as probability_distribution


class TestProbabilityDistribution(unittest.TestCase):
    def setUp(self) -> None:
        self._test_distribution_d4 = probability_distribution.ProbabilityDistribution.build_form_result_map(
            {1: 1, 2: 1, 3: 1, 4: 1}
        )
        self._test_distribution_2 = probability_distribution.ProbabilityDistribution.build_form_result_map(
            {2: 1}
        )

    def test_probability_distribution_get_result_map(self):
        self.assertEqual(
            {1: 1, 2: 1, 3: 1, 4: 1},
            self._test_distribution_d4.get_result_map()
        )

    def test_probability_distribution_get_dict_form(self):
        self.assertEqual(
            {1: 0.25, 2: 0.25, 3: 0.25, 4: 0.25},
            self._test_distribution_d4.get_dict_form()
        )

    def test_probability_distribution_add(self):
        test_distribution_one = self._test_distribution_d4 + self._test_distribution_2
        test_distribution_two = self._test_distribution_d4 + self._test_distribution_d4
        self.assertEqual(
            {3: 1, 4: 1, 5: 1, 6: 1},
            test_distribution_one.get_result_map()
        )
        self.assertEqual(
            {2: 1, 3: 2, 4: 3, 5: 4, 6: 3, 7: 2, 8: 1},
            test_distribution_two.get_result_map()
        )

    def test_probability_distribution_sub(self):
        test_distribution_one = self._test_distribution_d4 - self._test_distribution_2
        test_distribution_two = self._test_distribution_d4 - self._test_distribution_d4
        self.assertEqual(
            {-1: 1, 0: 1, 1: 1, 2: 1},
            test_distribution_one.get_result_map()
        )
        self.assertEqual(
            {-3: 1, -2: 2, -1: 3, 0: 4, 1: 3, 2: 2, 3: 1},
            test_distribution_two.get_result_map()
        )

    def test_probability_distribution_mul(self):
        test_distribution_one = self._test_distribution_d4 * self._test_distribution_2
        test_distribution_two = self._test_distribution_d4 * self._test_distribution_d4
        self.assertEqual(
            {2: 1, 4: 1, 6: 1, 8: 1},
            test_distribution_one.get_result_map()
        )
        self.assertEqual(
            {1: 1, 2: 2, 3: 2, 4: 3, 6: 2, 8: 2, 9: 1, 12: 2, 16: 1},
            test_distribution_two.get_result_map()
        )

    def test_probability_distribution_floordiv(self):
        test_distribution_one = self._test_distribution_d4 // self._test_distribution_2
        test_distribution_two = self._test_distribution_d4 // self._test_distribution_d4
        self.assertEqual(
            {0: 1, 1: 2, 2: 1},
            test_distribution_one.get_result_map()
        )
        self.assertEqual(
            {0: 6, 1: 6, 2: 2, 3: 1, 4: 1},
            test_distribution_two.get_result_map()
        )
