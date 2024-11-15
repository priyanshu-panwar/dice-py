<p align="center">
<a href="https://pepy.tech/projects/dicedb-py"><img src="https://static.pepy.tech/badge/dicedb-py" alt="PyPI Downloads"></a> <a href="https://pepy.tech/projects/dicedb-py"><img src="https://static.pepy.tech/badge/dicedb-py/month" alt="PyPI Downloads"></a>
</p>

# 🎲 DiceDB Python Client

Welcome to the **DiceDB Python Client**! This project provides an efficient way to interact with **DiceDB** using Python, managing connection pools and executing commands with ease.

## How to Install

```bash
pip install dicedb-py
```

OR

```bash
poetry add dicedb-py
```

## 📝 Usage

```bash
import asyncio

from dicedb_py import Dice


async def main():
    dice = Dice(host="localhost", port=7379)
    print(await dice.set("foo", "bar"))
    val = await dice.get("foo")
    print(val)


if __name__ == "__main__":
    asyncio.run(main())
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
