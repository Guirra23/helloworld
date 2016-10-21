import unittest
from fib import fib


class FibTestCase(unittest.TestCase):

    def test_fib1(self):
        self.assertEqual(fib(1), 1)

    def test_fib0(self):
        self.assertEqual(fib(0), 0)

    def test_fib6(self):
        self.assertEqual(fib(6), 8)

    def test_fib6_again(self):
        self.assertTrue(fib(6) == 8)


unittest.main()
