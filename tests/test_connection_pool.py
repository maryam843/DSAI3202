"""
Unit tests for connection pool.

Author: Maryam Mahaboob - 60301005
"""

import unittest
from src.connection_pool import ConnectionPool


class TestConnectionPool(unittest.TestCase):

    def setUp(self):
        self.pool = ConnectionPool(size=2)

    def test_get_connection(self):
        conn1 = self.pool.get_connection()
        conn2 = self.pool.get_connection()
        self.assertIn(conn1, ["DB_Conn_0", "DB_Conn_1"])
        self.assertIn(conn2, ["DB_Conn_0", "DB_Conn_1"])
        self.assertIsNone(self.pool.get_connection())

    def test_release_connection(self):
        conn = self.pool.get_connection()
        self.pool.release_connection(conn)
        conn2 = self.pool.get_connection()
        self.assertEqual(conn, conn2)


if __name__ == "__main__":
    unittest.main()
