import unittest

import src.constant_integer as constant_integer


class TestConstantInteger(unittest.TestCase):
    def setUp(self):
        self._test_constant_integers = constant_integer.ConstantInteger(14)

    def test_constant_integers_roll(self):
        for _ in range(100):
            self.assertEqual(14, self._test_constant_integers.roll())

    def test_constant_integers_max(self):
        self.assertEqual(14, self._test_constant_integers.max())

    def test_constant_integers_min(self):
        self.assertEqual(14, self._test_constant_integers.min())

    def test_constant_integers_str(self):
        self.assertEqual("14", str(self._test_constant_integers))
