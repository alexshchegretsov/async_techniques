# -*- coding: utf-8 -*-
import colorama
import datetime
import asyncio as aio
import uvloop


async def generate_data(num: int, data: aio.Queue):
    for idx in range(1, num + 1):
        await data.put((idx * idx, datetime.datetime.now()))
        await aio.sleep(0)


async def process_data(num: int, data: aio.Queue):
    processed = 0
    while processed < num:
        await data.get()
        processed += 1
        await aio.sleep(0)


async def main():
    lim = 250_000
    print(f"running built-in loop with limit {lim*2}")
    start = datetime.datetime.now()

    data = aio.Queue()

    task_1 = aio.create_task(generate_data(lim, data))
    task_2 = aio.create_task(generate_data(lim, data))
    task_3 = aio.create_task(process_data(lim*2, data))

    await aio.gather(task_1, task_2, task_3)

    print(f"overall time: {datetime.datetime.now() - start}")

if __name__ == '__main__':
    uvloop.install() # overall time: 0:00:13.276197 - uv_loop
    aio.run(main())