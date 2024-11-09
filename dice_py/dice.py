import logging

from .connection import DiceClient
from .command import Command

logging.basicConfig(level=logging.INFO)


class Dice(Command):
    def __init__(self, host: str, port: int, pool_size: int = 5):
        self.host = host
        self.port = port
        self.pool_size = pool_size
        self.client = DiceClient(host, port)
        super().__init__(self.client)
