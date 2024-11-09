import unittest
import asyncio
from dicedb_py.dice import Dice


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

    def test_delete(self):
        # First, set the key to ensure it exists
        self.loop.run_until_complete(self.dice.set("test_key", 10))
        delete_response = self.loop.run_until_complete(self.dice.delete("test_key"))
        self.assertTrue(delete_response)

    def test_exists(self):
        # First, set the key to ensure it exists
        self.loop.run_until_complete(self.dice.set("test_key", 10))
        exists_response = self.loop.run_until_complete(self.dice.exists("test_key"))
        self.assertTrue(exists_response)

    def test_not_exists(self):
        exists_response = self.loop.run_until_complete(self.dice.exists("test_key"))
        self.assertFalse(exists_response)

    async def test_expire(self):
        # First, set the key to ensure it exists
        self.loop.run_until_complete(self.dice.set("test_key", 10))
        expire_response = self.loop.run_until_complete(self.dice.expire("test_key", 10))
        self.assertTrue(expire_response)
        # Check if the key exists after 10 seconds
        asyncio.sleep(10)
        exists_response = self.loop.run_until_complete(self.dice.exists("test_key"))
        self.assertFalse(exists_response)

    async def test_keys(self):
        # First, set the key to ensure it exists
        self.loop.run_until_complete(self.dice.set("test_key", 10))
        self.loop.run_until_complete(self.dice.set("test_key_2", 20))
        keys_response = self.loop.run_until_complete(self.dice.keys("*"))
        self.assertIn(["test_key", "test_key_2"], keys_response)

    def test_flush(self):
        # First, set the key to ensure it exists
        self.loop.run_until_complete(self.dice.set("test_key", 10))
        self.loop.run_until_complete(self.dice.set("test_key_2", 20))
        flush_response = self.loop.run_until_complete(self.dice.flush())
        self.assertTrue(flush_response)

    def test_incr(self):
        # First, set the key to ensure it exists
        self.loop.run_until_complete(self.dice.set("test_key", 10))
        incr_response = self.loop.run_until_complete(self.dice.incr("test_key"))
        self.assertEqual(incr_response, 11)

    def test_decr(self):
        # First, set the key to ensure it exists
        self.loop.run_until_complete(self.dice.set("test_key", 10))
        decr_response = self.loop.run_until_complete(self.dice.decr("test_key"))
        self.assertEqual(decr_response, 9)

    def test_incrby(self):
        # First, set the key to ensure it exists
        self.loop.run_until_complete(self.dice.set("test_key", 10))
        incrby_response = self.loop.run_until_complete(self.dice.incrby("test_key", 5))
        self.assertEqual(incrby_response, 15)

    def test_decrby(self):
        # First, set the key to ensure it exists
        self.loop.run_until_complete(self.dice.set("test_key", 10))
        decrby_response = self.loop.run_until_complete(self.dice.decrby("test_key", 5))
        self.assertEqual(decrby_response, 5)

    def test_ttl_not_set(self):
        # First, set the key to ensure it exists
        self.loop.run_until_complete(self.dice.set("test_key", 10))
        ttl_response = self.loop.run_until_complete(self.dice.ttl("test_key"))
        self.assertEqual(ttl_response, -1)

    def test_ttl_set(self):
        # First, set the key to ensure it exists
        self.loop.run_until_complete(self.dice.set("test_key", 10))
        self.loop.run_until_complete(self.dice.expire("test_key", 10))
        ttl_response = self.loop.run_until_complete(self.dice.ttl("test_key"))
        self.assertEqual(ttl_response, 9)

    def test_ttl_not_exists(self):
        ttl_response = self.loop.run_until_complete(self.dice.ttl("test_key"))
        self.assertEqual(ttl_response, -2)

    def tearDown(self):
        # Clean up by deleting the test key
        self.loop.run_until_complete(self.dice._execute_command("DEL test_key"))
