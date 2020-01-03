# -*- coding: utf-8 -*-

import asyncio
import time

async def say_after(delay, what):
    print("before await sleep")
    await asyncio.sleep(delay)
    print(what)

async def main():
    print(f"started at {time.strftime('%X')}")

    # create tasks
    task_1 = asyncio.create_task(say_after(1, "hello"))
    task_2 = asyncio.create_task(say_after(2, "world"))

    # run tasks in event_loop
    await task_1
    await task_2
    print(f"finished at {time.strftime('%X')}")

if __name__ == '__main__':
    asyncio.run(main())