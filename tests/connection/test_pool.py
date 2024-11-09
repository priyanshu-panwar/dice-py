import unittest
from unittest.mock import patch, MagicMock
from dice_py.connection.pool import ConnectionPool
from dice_py.connection.connect import Connect


class TestConnectionPool(unittest.TestCase):

    @patch("dice_py.connection.pool.Connect")
    def test_init_pool(self, MockConnect):
        mock_conn = MagicMock(spec=Connect)
        MockConnect.return_value = mock_conn

        pool = ConnectionPool("localhost", 7379, pool_size=3)

        self.assertEqual(len(pool.pool), 3)
        self.assertTrue(all(isinstance(conn, MagicMock) for conn in pool.pool))

    @patch("dice_py.connection.pool.Connect")
    def test_get_new_connection(self, MockConnect):
        mock_conn = MagicMock(spec=Connect)
        MockConnect.return_value = mock_conn

        pool = ConnectionPool("localhost", 7379)
        conn = pool.get_new_connection()

        self.assertIsInstance(conn, MagicMock)
        self.assertEqual(
            mock_conn.connect.call_count, 6
        )  # 5 from init_pool and 1 from get_new_connection

    @patch("dice_py.connection.pool.Connect")
    def test_return_connection(self, MockConnect):
        mock_conn = MagicMock(spec=Connect)
        MockConnect.return_value = mock_conn

        pool = ConnectionPool("localhost", 7379, pool_size=1)
        conn = pool.pool.pop()
        pool._return_connection(conn)

        self.assertEqual(len(pool.pool), 1)
        pool._return_connection(conn)
        mock_conn.close.assert_called_once()

    @patch("dice_py.connection.pool.Connect")
    def test_close_all(self, MockConnect):
        mock_conn = MagicMock(spec=Connect)
        MockConnect.return_value = mock_conn

        pool = ConnectionPool("localhost", 7379, pool_size=3)
        pool.close_all()

        self.assertEqual(len(pool.pool), 0)
        self.assertEqual(mock_conn.close.call_count, 3)

    @patch("dice_py.connection.pool.Connect")
    async def test_get(self, MockConnect):
        mock_conn = MagicMock(spec=Connect)
        MockConnect.return_value = mock_conn

        pool = ConnectionPool("localhost", 7379, pool_size=1)
        async with pool.get() as conn:
            self.assertIsInstance(conn, MagicMock)

        self.assertEqual(len(pool.pool), 1)
