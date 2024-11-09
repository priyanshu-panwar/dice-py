from ..connection.pool import ConnectionPool


class DiceClient:
    def __init__(self, host: str, port: int, pool_size: int = 5):
        self.pool = ConnectionPool(host, port, pool_size)
