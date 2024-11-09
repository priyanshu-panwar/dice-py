import logging

from ..connection.client import DiceClient
from ..connection.connect import Connect
from ..utils import to_resp


_logger = logging.getLogger(__name__)


class Executor:
    def __init__(self, client: DiceClient):
        self.client = client

    def _send_command(self, command: str, conn: Connect):
        """Send a command to the socket."""
        conn.sock.sendall(command.encode("utf-8"))
        response = conn.sock.recv(4096).decode("utf-8")
        return response.split("\r\n")[0][1:]

    async def _execute_command(self, command: str):
        """Execute a command using an available connection from the pool."""
        try:
            command = to_resp(command)
            async with self.client.pool.get() as conn:
                try:
                    return self._send_command(command, conn)
                except OSError as e:
                    if e.errno == 9:
                        _logger.error("Connection closed by the server.")
                        conn = self.client.pool.get_new_connection()
                        return self._send_command(command, conn)
                    else:
                        raise e
        except Exception as e:
            _logger.error(f"Error executing command: {e}")
            raise e
