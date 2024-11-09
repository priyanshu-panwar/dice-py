# 🎲 DiceDB Python Client

Welcome to the **DiceDB Python Client**! This project provides an efficient way to interact with **DiceDB** using Python, managing connection pools and executing commands with ease.

## 📝 Usage

```bash
import asyncio
from dicedb_py import Dice


async def test():
    dice = Dice("localhost", 7379)

    import time, random

    start_time = time.time()
    while (time.time() - start_time) < 600:
        x = await dice.set("foo", "bar")
        print(x)
        val = await dice.get("foo")
        print(val)
        sleep = random.randint(15, 30)
        print(f"Sleeping for {sleep} seconds.")
        await asyncio.sleep(sleep)


asyncio.run(test())

```

## 🛠️ Commands

- `SET`: set key-value
  Ex: `await dice.set("key", "val)`

- `GET`: get value from key
  Ex: `await dice.get("key")`

- `DEL`: delete key
  Ex: `await dice.delete("key")`

- `EXISTS`: check if a key exists & returns bool
  Ex: `await dice.exists("key")`

- `EXPIRE`: sets ttl in seconds for a key
  Ex: `await dice.expire("key", 10)`

- `KEYS`: get all keys in a list according to the pattern give. Use "_" for all keys.
  Ex: `await dice.keys("_")`

- `FLUSH`: clear all keys
  Ex: `await dice.flush()`

- `INCR`: incr key by 1. Default value to start is 0 if key is not already set.
  Ex: `await dice.incr("key")`

- `INCRBY`: incr key by amount (int)
  Ex: `await dice.incrby("key", 2)`

- `DECR`: decr key by 1.
  Ex: `await dice.decr("key")`

- `DECRBY`: decr key by amount (int)
  Ex: `await dice.decrby("key", 2)`

- `TTL`: get TTL (time to live) of the key in seconds
  Ex: `await dice.ttl("key")`
