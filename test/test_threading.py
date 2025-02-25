import unittest
from src.threading import parallel_thread_sum

class TestThreadingSum(unittest.TestCase):
    def test_sum(self):
        self.assertEqual(parallel_thread_sum(10, 2), 55)

if __name__ == '__main__':
    unittest.main()


