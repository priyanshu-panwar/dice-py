import unittest
from dicedb_py.utils import to_resp


class TestToResp(unittest.TestCase):

    def test_ping(self):
        command = "PING"
        expected_resp = "*1\r\n$4\r\nPING\r\n"
        self.assertEqual(to_resp(command), expected_resp)

    def test_set_key_value(self):
        command = "SET key value"
        expected_resp = "*3\r\n$3\r\nSET\r\n$3\r\nkey\r\n$5\r\nvalue\r\n"
        self.assertEqual(to_resp(command), expected_resp)

    def test_empty_command(self):
        command = ""
        expected_resp = "*1\r\n$0\r\n\r\n"
        self.assertEqual(to_resp(command), expected_resp)

    def test_get_key_special_chars(self):
        command = "GET key!@#"
        expected_resp = "*2\r\n$3\r\nGET\r\n$6\r\nkey!@#\r\n"
        self.assertEqual(to_resp(command), expected_resp)

    def test_multiple_words(self):
        command = "MULTI WORD COMMAND"
        expected_resp = "*3\r\n$5\r\nMULTI\r\n$4\r\nWORD\r\n$7\r\nCOMMAND\r\n"
        self.assertEqual(to_resp(command), expected_resp)

    def test_single_word(self):
        command = "WORD"
        expected_resp = "*1\r\n$4\r\nWORD\r\n"
        self.assertEqual(to_resp(command), expected_resp)

    def test_special_characters(self):
        command = "SPECIAL !@# $%^"
        expected_resp = "*3\r\n$7\r\nSPECIAL\r\n$3\r\n!@#\r\n$3\r\n$%^\r\n"
        self.assertEqual(to_resp(command), expected_resp)
