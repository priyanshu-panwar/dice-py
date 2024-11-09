import asyncio
import unittest
from unittest.mock import patch, MagicMock
from dice_py.connection.client import DiceClient
from dice_py.connection.connect import Connect
from dice_py.command.executor import Executor


class TestExecutor(unittest.TestCase):

    @patch("dice_py.command.executor.Connect")
    def test_send_command(self, mock_connect):
        mock_conn = MagicMock(spec=Connect)
        mock_conn.sock = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.sock.recv.return_value = b"+PONG\r\n"

        executor = Executor(MagicMock(spec=DiceClient))
        response = executor._send_command("PING", mock_conn)

        mock_conn.sock.sendall.assert_called_once_with(b"PING")
        mock_conn.sock.recv.assert_called_once_with(4096)
        self.assertEqual(response, "PONG")

    @patch("dice_py.command.executor.to_resp", return_value="*1\r\n$4\r\nPING\r\n")
    @patch("dice_py.command.executor.Executor._send_command", return_value="PONG")
    @patch("dice_py.command.executor.DiceClient")
    def test_execute_command(self, mock_client, mock_send_command, mock_to_resp):
        mock_conn = MagicMock(spec=Connect)
        mock_client.pool.get.return_value.__aenter__.return_value = mock_conn

        executor = Executor(mock_client)
        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(executor._execute_command("PING"))

        mock_to_resp.assert_called_once_with("PING")
        mock_send_command.assert_called_once_with("*1\r\n$4\r\nPING\r\n", mock_conn)
        self.assertEqual(response, "PONG")

    @patch("dice_py.command.executor.to_resp", return_value="*1\r\n$4\r\nPING\r\n")
    @patch(
        "dice_py.command.executor.Executor._send_command",
        side_effect=OSError(9, "Bad file descriptor"),
    )
    @patch("dice_py.command.executor.DiceClient")
    def test_execute_command_reconnect(
        self, mock_client, mock_send_command, mock_to_resp
    ):
        mock_conn = MagicMock(spec=Connect)
        mock_client.pool.get.return_value.__aenter__.return_value = mock_conn
        mock_client.pool.get_new_connection.return_value = mock_conn
        mock_send_command.side_effect = [OSError(9, "Bad file descriptor"), "PONG"]

        executor = Executor(mock_client)
        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(executor._execute_command("PING"))

        mock_to_resp.assert_called_once_with("PING")
        self.assertEqual(mock_send_command.call_count, 2)
        mock_client.pool.get_new_connection.assert_called_once()
        self.assertEqual(response, "PONG")

    @patch("dice_py.command.executor.to_resp", return_value="*1\r\n$4\r\nPING\r\n")
    @patch(
        "dice_py.command.executor.Executor._send_command",
        side_effect=Exception("Test Exception"),
    )
    @patch("dice_py.command.executor.DiceClient")
    def test_execute_command_exception(
        self, mock_client, mock_send_command, mock_to_resp
    ):
        mock_conn = MagicMock(spec=Connect)
        mock_client.pool.get.return_value.__aenter__.return_value = mock_conn

        executor = Executor(mock_client)
        loop = asyncio.get_event_loop()
        with self.assertRaises(Exception) as context:
            loop.run_until_complete(executor._execute_command("PING"))

        mock_to_resp.assert_called_once_with("PING")
        mock_send_command.assert_called_once_with("*1\r\n$4\r\nPING\r\n", mock_conn)
        self.assertTrue("Test Exception" in str(context.exception))
