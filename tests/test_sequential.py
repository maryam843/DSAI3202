import unittest
from main import sequential_sum

class TestSequentialSum(unittest.TestCase):
    def test_sum(self):
        self.assertEqual(sequential_sum(10), 55)

if __name__ == '__main__':
    unittest.main()
