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

    async def delete(self, key) -> bool:
        """Delete a key."""
        return await self._execute_command(f"DEL {key}") == "1"

    async def exists(self, key) -> bool:
        """Check if a key exists."""
        return await self._execute_command(f"EXISTS {key}") == "1"

    async def expire(self, key: str, seconds: int) -> bool:
        """Set a timeout on a key."""
        return await self._execute_command(f"EXPIRE {key} {seconds}") == "1"

    async def keys(self, pattern: str) -> list:
        """
        Get all keys matching a pattern.
        The pattern is a glob-style pattern. Use * as a wildcard for any number of characters.
        """
        keys = await self._execute_command(f"KEYS {pattern}")
        return keys.split(" ") if keys else []

    async def flush(self) -> bool:
        """Delete all keys."""
        return await self._execute_command("FLUSHDB") == "OK"

    async def incr(self, key) -> int:
        """Increment the value of a key."""
        return int(await self._execute_command(f"INCR {key}"))

    async def decr(self, key) -> int:
        """Decrement the value of a key."""
        return int(await self._execute_command(f"DECR {key}"))

    async def incrby(self, key: str, amount: int) -> int:
        """Increment the value of a key by a specified amount."""
        return int(await self._execute_command(f"INCRBY {key} {amount}"))

    async def decrby(self, key: str, amount: int) -> int:
        """Decrement the value of a key by a specified amount."""
        return int(await self._execute_command(f"DECRBY {key} {amount}"))

    async def ttl(self, key: str) -> int:
        """
        Get the time to live for a key.
        positive integer: the remaining time to live in seconds
        -2: the key does not exist
        -1: the key exists but has no associated expire
        """
        return int(await self._execute_command(f"TTL {key}"))
