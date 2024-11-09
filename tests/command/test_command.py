import unittest
from unittest.mock import patch, MagicMock
from dice_py.command.command import Command
from dice_py.connection.client import DiceClient
import asyncio


class TestCommand(unittest.TestCase):

    def setUp(self):
        self.client = MagicMock(spec=DiceClient)
        self.command = Command(self.client)
        self.loop = asyncio.get_event_loop()

    @patch("dice_py.command.executor.Executor._execute_command", return_value="OK")
    def test_set(self, mock_execute_command):
        set_response = self.loop.run_until_complete(
            self.command.set("test_key", "test_value")
        )
        mock_execute_command.assert_called_once_with("SET test_key test_value")
        self.assertEqual(set_response, "OK")

    @patch(
        "dice_py.command.executor.Executor._execute_command", return_value="test_value"
    )
    def test_get(self, mock_execute_command):
        get_response = self.loop.run_until_complete(self.command.get("test_key"))
        mock_execute_command.assert_called_once_with("GET test_key")
        self.assertEqual(get_response, "test_value")

    @patch("dice_py.command.executor.Executor._execute_command", return_value="1")
    def test_delete(self, mock_execute_command):
        delete_response = self.loop.run_until_complete(self.command.delete("test_key"))
        mock_execute_command.assert_called_once_with("DEL test_key")
        self.assertTrue(delete_response)

    @patch("dice_py.command.executor.Executor._execute_command", return_value="1")
    def test_exists(self, mock_execute_command):
        exists_response = self.loop.run_until_complete(self.command.exists("test_key"))
        mock_execute_command.assert_called_once_with("EXISTS test_key")
        self.assertTrue(exists_response)

    @patch("dice_py.command.executor.Executor._execute_command", return_value="1")
    def test_expire(self, mock_execute_command):
        expire_response = self.loop.run_until_complete(
            self.command.expire("test_key", 60)
        )
        mock_execute_command.assert_called_once_with("EXPIRE test_key 60")
        self.assertTrue(expire_response)

    @patch(
        "dice_py.command.executor.Executor._execute_command",
        return_value="test_key test_key_2",
    )
    def test_keys(self, mock_execute_command):
        keys_response = self.loop.run_until_complete(self.command.keys("*"))
        mock_execute_command.assert_called_once_with("KEYS *")
        self.assertEqual(keys_response, ["test_key", "test_key_2"])

    @patch(
        "dice_py.command.executor.Executor._execute_command",
        return_value="OK",
    )
    def test_flush(self, mock_execute_command):
        flush_response = self.loop.run_until_complete(self.command.flush())
        mock_execute_command.assert_called_once_with("FLUSHDB")
        self.assertTrue(flush_response)

    @patch("dice_py.command.executor.Executor._execute_command", return_value="11")
    def test_incr(self, mock_execute_command):
        incr_response = self.loop.run_until_complete(self.command.incr("test_key"))
        mock_execute_command.assert_called_once_with("INCR test_key")
        self.assertEqual(incr_response, 11)

    @patch("dice_py.command.executor.Executor._execute_command", return_value="9")
    def test_decr(self, mock_execute_command):
        decr_response = self.loop.run_until_complete(self.command.decr("test_key"))
        mock_execute_command.assert_called_once_with("DECR test_key")
        self.assertEqual(decr_response, 9)

    @patch("dice_py.command.executor.Executor._execute_command", return_value="11")
    def test_incrby(self, mock_execute_command):
        _ = self.loop.run_until_complete(self.command.set("test_key", 6))
        incrby_response = self.loop.run_until_complete(
            self.command.incrby("test_key", 5)
        )
        self.assertEqual(incrby_response, 11)

    @patch("dice_py.command.executor.Executor._execute_command", return_value="1")
    def test_decrby(self, mock_execute_command):
        _ = self.loop.run_until_complete(self.command.set("test_key", 6))
        decrby_response = self.loop.run_until_complete(
            self.command.decrby("test_key", 5)
        )
        self.assertEqual(decrby_response, 1)

    @patch("dice_py.command.executor.Executor._execute_command", return_value="-1")
    def test_ttl_not_set(self, mock_execute_command):
        _ = self.loop.run_until_complete(self.command.set("test_key", 10))
        ttl_response = self.loop.run_until_complete(self.command.ttl("test_key"))
        self.assertEqual(ttl_response, -1)

    @patch("dice_py.command.executor.Executor._execute_command", return_value="10")
    def test_ttl(self, mock_execute_command):
        _ = self.loop.run_until_complete(self.command.set("test_key", 10))
        _ = self.loop.run_until_complete(self.command.expire("test_key", 10))
        ttl_response = self.loop.run_until_complete(self.command.ttl("test_key"))
        self.assertEqual(ttl_response, 10)
