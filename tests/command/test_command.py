import unittest
from unittest.mock import patch
from dice_py.command.command import Command
import asyncio


class TestCommand(unittest.TestCase):

    @patch("dice_py.command.executor.Executor._execute_command", return_value="OK")
    @patch("dice_py.command.executor.DiceClient")
    def test_set(self, mock_client, mock_execute_command):
        command = Command(mock_client)
        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(command.set("key", "value"))

        mock_execute_command.assert_called_once_with("SET key value")
        self.assertEqual(response, "OK")

    @patch("dice_py.command.executor.Executor._execute_command", return_value="value")
    @patch("dice_py.command.executor.DiceClient")
    def test_get(self, mock_client, mock_execute_command):
        command = Command(mock_client)
        loop = asyncio.get_event_loop()
        response = loop.run_until_complete(command.get("key"))

        mock_execute_command.assert_called_once_with("GET key")
        self.assertEqual(response, "value")
