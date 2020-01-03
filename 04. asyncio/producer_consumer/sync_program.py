# -*- coding: utf-8 -*-
import colorama
import datetime
import random
import time


def generate_task(num: int, tasks: list):
    for idx in range(1, num + 1):
        item = idx ** 2
        tasks.append((item, datetime.datetime.now()))

        print(f"{colorama.Fore.YELLOW} --- generated item {idx}", flush=True)
        time.sleep(random.random() + 0.5)


def process_task(num: int, tasks: list):
    processed = 0
    overall_time = datetime.timedelta(0, 0, 0, 0, 0, 0, 0)

    while processed < num:
        task = tasks.pop(0)
        item, t = task
        processed += 1
        delta = datetime.datetime.now() - t
        overall_time += delta
        print(f"{colorama.Fore.CYAN} +++ processed value {item} after {delta.total_seconds()} sec.,\
        average {overall_time/processed}")
        time.sleep(0.5)


def main():
    t0 = datetime.datetime.now()
    print(f"{colorama.Fore.WHITE} App started", flush=True)
    # list of tasks?
    tasks = []
    # synchronous code
    generate_task(20, tasks)  # first do all generating
    process_task(20, tasks)  # do all processing after generating

    print(f"Overall time is {datetime.datetime.now() - t0}")


if __name__ == '__main__':
    main()
