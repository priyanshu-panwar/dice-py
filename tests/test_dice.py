import unittest
import asyncio
from dice_py.dice import Dice


class TestDice(unittest.TestCase):

    def setUp(self):
        self.dice = Dice(host="localhost", port=7379)
        self.loop = asyncio.get_event_loop()

    def test_set(self):
        set_response = self.loop.run_until_complete(
            self.dice.set("test_key", "test_value")
        )
        self.assertEqual(set_response, "OK")

    def test_get(self):
        # First, set the key to ensure it exists
        self.loop.run_until_complete(self.dice.set("test_key", 10))
        get_response = self.loop.run_until_complete(self.dice.get("test_key"))
        self.assertEqual(get_response, "10")

    def tearDown(self):
        # Clean up by deleting the test key
        self.loop.run_until_complete(self.dice._execute_command("DEL test_key"))
