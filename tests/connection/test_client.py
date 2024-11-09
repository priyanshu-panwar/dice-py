import unittest
from unittest.mock import patch, MagicMock
from dicedb_py.connection.client import DiceClient
from dicedb_py.connection.pool import ConnectionPool


class TestDiceClient(unittest.TestCase):

    @patch("dicedb_py.connection.client.ConnectionPool")
    def test_init(self, MockConnectionPool):
        mock_pool = MagicMock(spec=ConnectionPool)
        MockConnectionPool.return_value = mock_pool

        client = DiceClient("localhost", 7379, pool_size=5)

        MockConnectionPool.assert_called_once_with("localhost", 7379, 5)
        self.assertEqual(client.pool, mock_pool)
