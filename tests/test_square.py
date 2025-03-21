"""
Unit tests for parallel square functions.

Author: Maryam Mahaboob - 60301005
"""

import unittest
from src.square import (
    square,
    sequential_squares,
    multiprocessing_squares,
    pool_map,
    pool_apply,
    concurrent_futures
)


class TestSquareFunctions(unittest.TestCase):

    def setUp(self):
        self.numbers = list(range(10))
        self.expected = [n * n for n in self.numbers]

    def test_square(self):
        self.assertEqual(square(4), 16)

    def test_sequential_squares(self):
        self.assertEqual(sequential_squares(self.numbers), self.expected)

    def test_multiprocessing_squares(self):
        self.assertEqual(multiprocessing_squares(self.numbers), self.expected)

    def test_pool_map(self):
        self.assertEqual(pool_map(self.numbers), self.expected)

    def test_pool_apply(self):
        self.assertEqual(pool_apply(self.numbers), self.expected)

    def test_concurrent_futures(self):
        self.assertEqual(concurrent_futures(self.numbers), self.expected)


if __name__ == "__main__":
    unittest.main()
