import pathlib
import unittest

import PIL.Image as Image
import PIL.ImageChops as ImageChops

import python_dice.src.probability_distribution as probability_distribution


class TestProbabilityDistribution(unittest.TestCase):
    def setUp(self) -> None:
        self._test_distribution_d4 = probability_distribution.ProbabilityDistribution(
            {1: 1, 2: 1, 3: 1, 4: 1}
        )
        self._test_distribution_2 = probability_distribution.ProbabilityDistribution(
            {2: 1}
        )

    def test_probability_distribution_get_result_map(self):
        self.assertEqual(
            {1: 1, 2: 1, 3: 1, 4: 1}, self._test_distribution_d4.get_result_map()
        )

    def test_probability_distribution_get_dict_form(self):
        self.assertEqual(
            {1: 0.25, 2: 0.25, 3: 0.25, 4: 0.25},
            self._test_distribution_d4.get_dict_form(),
        )

    def test_probability_distribution_add(self):
        test_distribution_one = self._test_distribution_d4 + self._test_distribution_2
        test_distribution_two = self._test_distribution_d4 + self._test_distribution_d4
        self.assertEqual(
            {3: 1, 4: 1, 5: 1, 6: 1}, test_distribution_one.get_result_map()
        )
        self.assertEqual(
            {2: 1, 3: 2, 4: 3, 5: 4, 6: 3, 7: 2, 8: 1},
            test_distribution_two.get_result_map(),
        )

    def test_probability_distribution_sub(self):
        test_distribution_one = self._test_distribution_d4 - self._test_distribution_2
        test_distribution_two = self._test_distribution_d4 - self._test_distribution_d4
        self.assertEqual(
            {-1: 1, 0: 1, 1: 1, 2: 1}, test_distribution_one.get_result_map()
        )
        self.assertEqual(
            {-3: 1, -2: 2, -1: 3, 0: 4, 1: 3, 2: 2, 3: 1},
            test_distribution_two.get_result_map(),
        )

    def test_probability_distribution_mul(self):
        test_distribution_one = self._test_distribution_d4 * self._test_distribution_2
        test_distribution_two = self._test_distribution_d4 * self._test_distribution_d4
        self.assertEqual(
            {2: 1, 4: 1, 6: 1, 8: 1}, test_distribution_one.get_result_map()
        )
        self.assertEqual(
            {1: 1, 2: 2, 3: 2, 4: 3, 6: 2, 8: 2, 9: 1, 12: 2, 16: 1},
            test_distribution_two.get_result_map(),
        )

    def test_probability_distribution_floordiv(self):
        test_distribution_one = self._test_distribution_d4 // self._test_distribution_2
        test_distribution_two = self._test_distribution_d4 // self._test_distribution_d4
        self.assertEqual({0: 1, 1: 2, 2: 1}, test_distribution_one.get_result_map())
        self.assertEqual(
            {0: 6, 1: 6, 2: 2, 3: 1, 4: 1}, test_distribution_two.get_result_map()
        )

    def test_probability_distribution_max(self):
        test_distribution_one = self._test_distribution_d4 * self._test_distribution_2
        test_distribution_two = self._test_distribution_d4 - self._test_distribution_d4
        self.assertEqual(8, test_distribution_one.max())
        self.assertEqual(3, test_distribution_two.max())

    def test_probability_distribution_min(self):
        test_distribution_one = self._test_distribution_d4 * self._test_distribution_d4
        test_distribution_two = self._test_distribution_d4 - self._test_distribution_d4
        self.assertEqual(1, test_distribution_one.min())
        self.assertEqual(-3, test_distribution_two.min())

    def test_probability_distribution_contains_zero(self):
        test_distribution_one = self._test_distribution_d4 * self._test_distribution_d4
        test_distribution_two = self._test_distribution_d4 - self._test_distribution_d4
        self.assertEqual(False, test_distribution_one.contains_zero())
        self.assertEqual(True, test_distribution_two.contains_zero())

    def test_probability_distribution_eq(self):
        test_distribution = self._test_distribution_d4 == self._test_distribution_d4
        self.assertEqual({0: 12, 1: 4}, test_distribution.get_result_map())

    def test_probability_distribution_ne(self):
        test_distribution = self._test_distribution_d4 != self._test_distribution_d4
        self.assertEqual({0: 4, 1: 12}, test_distribution.get_result_map())

    def test_probability_distribution_lt(self):
        test_distribution = self._test_distribution_d4 < self._test_distribution_d4
        self.assertEqual({0: 10, 1: 6}, test_distribution.get_result_map())

    def test_probability_distribution_le(self):
        test_distribution = self._test_distribution_d4 <= self._test_distribution_d4
        self.assertEqual({0: 6, 1: 10}, test_distribution.get_result_map())

    def test_probability_distribution_gt(self):
        test_distribution = self._test_distribution_d4 < self._test_distribution_d4
        self.assertEqual({0: 10, 1: 6}, test_distribution.get_result_map())

    def test_probability_distribution_ge(self):
        test_distribution = self._test_distribution_d4 <= self._test_distribution_d4
        self.assertEqual({0: 6, 1: 10}, test_distribution.get_result_map())

    def test_probability_distribution_not_operator(self):
        test_distribution_d4_less_one = probability_distribution.ProbabilityDistribution(
            {0: 1, 1: 1, 2: 1, 3: 1}
        )
        test_distribution = test_distribution_d4_less_one.not_operator()
        self.assertEqual({0: 3, 1: 1}, test_distribution.get_result_map())

    def test_probability_distribution_and(self):
        test_distribution_d2_less_one = probability_distribution.ProbabilityDistribution(
            {0: 1, 1: 1}
        )
        test_distribution = self._test_distribution_d4.__and__(
            test_distribution_d2_less_one
        )
        self.assertEqual({0: 6, 1: 2}, test_distribution.get_result_map())

    def test_probability_distribution_or(self):
        test_distribution_d2_less_one = probability_distribution.ProbabilityDistribution(
            {0: 1, 1: 1}
        )
        test_distribution = test_distribution_d2_less_one.__or__(
            test_distribution_d2_less_one
        )
        self.assertEqual({0: 1, 1: 3}, test_distribution.get_result_map())

    def test_get_histogram(self):
        test_distribution = probability_distribution.ProbabilityDistribution(
            {1: 1, 2: 3, 3: 6, 4: 1}
        )
        image_path = pathlib.Path(
            pathlib.Path.cwd(),
            "python_dice",
            "test",
            "test_image",
            "TestProbabilityDistribution_test_get_histogram.png",
        )
        image = test_distribution.get_histogram()
        expected_image = Image.open(image_path)
        self.assertIsNone(ImageChops.difference(expected_image, image).getbbox())
