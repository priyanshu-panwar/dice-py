from .executor import Executor


class Command(Executor):

    def __init__(self, client):
        super().__init__(client)

    async def get(self, key) -> str:
        """Get the value of a key."""
        return await self._execute_command(f"GET {key}")

    async def set(self, key, value) -> str:
        """Set the value of a key."""
        return await self._execute_command(f"SET {key} {value}")
