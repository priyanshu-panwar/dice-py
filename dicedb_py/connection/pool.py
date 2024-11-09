from contextlib import asynccontextmanager
import logging
from collections import deque

from ..connection.connect import Connect


_logger = logging.getLogger(__name__)


class ConnectionPool:
    def __init__(self, host: str, port: int, pool_size: int = 5):
        self.host = host
        self.port = port
        self.pool_size = pool_size
        self.pool: deque[Connect] = deque()
        self._init_pool()

    def _init_pool(self):
        """Initialize the connection pool."""
        _logger.info(f"Initializing connection pool with {self.pool_size} connections.")
        for _ in range(self.pool_size):
            self.pool.append(self.get_new_connection())

    def get_new_connection(self) -> Connect:
        """Get a new connection."""
        conn = Connect(self.host, self.port)
        conn.connect()
        return conn

    async def _get_connection(self) -> Connect:
        """Get an available connection from the pool."""
        return self.pool.pop() if self.pool else None

    def _return_connection(self, conn: Connect):
        """Return a connection back to the pool."""
        if len(self.pool) < self.pool_size:
            self.pool.append(conn)
        else:
            conn.close()

    @asynccontextmanager
    async def get(self) -> any:
        """Get a connection from the pool."""
        try:
            conn = await self._get_connection()
            yield conn
        finally:
            self._return_connection(conn)

    def close_all(self):
        """Close all connections in the pool."""
        while self.pool:
            conn = self.pool.pop()
            conn.close()
