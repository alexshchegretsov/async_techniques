# -*- coding: utf-8 -*-


def fib():
    # 3 compute curr and return it with yield
    curr, nxt = 1, 1
    while True:
        # 7 compute another curr and yield it
        curr, nxt = nxt, curr + nxt
        yield curr


res = fib()                 # 1 create generator

for i in res:               # 2 6 call __next__ on res
    print(i, end=", ")      # 4 8 i=yielded value, print i
    if i > 50000:           # 5 9 do compare
        break
