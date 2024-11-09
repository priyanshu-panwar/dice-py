import socket
import logging

from ..utils import to_resp

_logger = logging.getLogger(__name__)


class Connect:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.sock.connect((self.host, self.port))
        _logger.info("Connected to Dicedb.")

    def close(self):
        self.sock.close()
        _logger.info("Connection closed.")

    def ping(self):
        try:
            command = to_resp("PING")
            self.sock.sendall(command.encode("utf-8"))
            response = self.sock.recv(4096).decode("utf-8")
            return response == "+PONG\r\n"
        except Exception as e:
            _logger.error(f"Error occured during ping: {e}")
            return False
