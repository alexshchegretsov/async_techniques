# -*- coding: utf-8 -*-
import uvloop

import colorama
import datetime
import random
import asyncio


# делим тело корутины на кусочки при помощи await в местах ожидания
async def generate_task(num: int, tasks: asyncio.Queue):
    for idx in range(1, num + 1):
        item = idx ** 2
        # пока мы добавляем в очередь - можно передать управление и что-то сделать
        # .put() - awaitable
        await tasks.put((item, datetime.datetime.now()))
        print(f"{colorama.Fore.YELLOW} --- generated item {idx}", flush=True)
        # пока спим - передаём управление и что-то делаем
        await asyncio.sleep(random.random() + 0.5)


async def process_task(num: int, tasks: asyncio.Queue):
    processed = 0
    while processed < num:
        # пока получаем из очереди элемент - передаём управление и что-то делаем
        # .get() - awaitable
        task = await tasks.get()
        item, t = task
        processed += 1
        delta = datetime.datetime.now() - t
        print(f"{colorama.Fore.CYAN} +++ processed value {item} after {delta.total_seconds()} sec.")
        # пока спим - передаём управление и что-то делаем
        await asyncio.sleep(0.5)


async def main():
    t0 = datetime.datetime.now()
    print(f"{colorama.Fore.WHITE} App started", flush=True)

    # queue of tasks
    tasks = asyncio.Queue()

    # create tasks
    task_1 = asyncio.create_task(generate_task(20, tasks))
    task_2 = asyncio.create_task(process_task(20, tasks))

    # asyncio.gather()
    # Return a future aggregating results from the given coroutines/futures.
    # Coroutines will be wrapped in a future and scheduled in the event
    # loop. They will not necessarily be scheduled in the same order as
    # passed in.
    # All futures must share the same event loop.  If all the tasks are
    # done successfully, the returned future's result is the list of
    # results (in the order of the original sequence, not necessarily
    # the order of results arrival).  If *return_exceptions* is True,
    # exceptions in the tasks are treated the same as successful
    # results, and gathered in the result list; otherwise, the first
    # raised exception will be immediately propagated to the returned
    # future
    # Cancellation: if the outer Future is cancelled, all children (that
    # have not completed yet) are also cancelled.  If any child is
    # cancelled, this is treated as if it raised CancelledError --
    # the outer Future is *not* cancelled in this case.
    # (This is to prevent the cancellation of one child to cause other
    # children to be cancelled.)
    await asyncio.gather(task_1, task_2)

    print(f"Overall time is {datetime.datetime.now() - t0}")


if __name__ == '__main__':
    # This function always creates a new event loop and closes it at the end.
    # It should be used as a main entry point for asyncio programs,
    # and should ideally only be called once.
    asyncio.run(main())
