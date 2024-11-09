# 🎲 DiceDB Python Client

Welcome to the **DiceDB Python Client**! This project provides an efficient way to interact with **DiceDB** using Python, managing connection pools and executing commands with ease.

## 📝 Usage

```bash
import asyncio
from dice_py import Dice


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
