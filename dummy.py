import asyncio
from dicedb_py import Dice


async def test():
    dice = Dice("localhost", 7379)

    import time, random

    start_time = time.time()
    while (time.time() - start_time) < 600:
        # x = await dice.set("foo", "bar")
        # print(x)
        # val = await dice.get("foo")
        # print(val)
        # x = await dice.delete("foo")
        # print(x)
        # y = await dice.keys("*")
        # print(y)
        print(await dice.incr("counter"))
        print(await dice.incr("counter"))
        print(await dice.incr("counter"))
        print(await dice.decr("counter"))
        sleep = random.randint(15, 30)
        print(f"Sleeping for {sleep} seconds.")
        await asyncio.sleep(sleep)


asyncio.run(test())
