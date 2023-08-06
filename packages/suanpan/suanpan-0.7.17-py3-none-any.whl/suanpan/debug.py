# coding=utf-8
from __future__ import print_function

import functools
import itertools
import math
import time

from suanpan import asyncio
from suanpan.log import logger
from suanpan.utils import term


def formatFuncCall(func, *args, **kwargs):
    paramString = ", ".join(
        itertools.chain(
            (str(a) for a in args), ("{}={}".format(k, v) for k, v in kwargs.items())
        )
    )
    funcString = "{}({})".format(func.__name__, paramString)
    return funcString


def costCall(func, *args, **kwargs):
    startTime = time.time()
    result = func(*args, **kwargs)
    endTime = time.time()
    costTime = endTime - startTime
    return costTime, result


def cost(func):
    @functools.wraps(func)
    def _dec(*args, **kwargs):
        costTime, result = costCall(func, *args, **kwargs)
        logger.info("{} - {}s".format(formatFuncCall(func, *args, **kwargs), costTime))
        return result

    return _dec


def abtest(
    func,
    number,
    concurrency=1,
    thread=True,
    args=None,
    kwargs=None,
    title="ABTest",
    funcName=None,
    markPercentages=(0.5, 0.66, 0.75, 0.8, 0.9, 0.95, 0.98, 0.99, 1),
):
    args = args or []
    kwargs = kwargs or {}
    testFunc = lambda x: costCall(func, *args, **kwargs)
    funcName = funcName or func.__name__
    func.__name__ = funcName
    results = asyncio.map(
        testFunc, range(number), workers=concurrency, thread=thread, pbar=title
    )
    costTimes = sorted(round(r[0] * 1000, 3) for r in results)
    totalTime = sum(costTimes)
    avgTime = totalTime / number
    minTime = min(costTimes)
    maxTime = max(costTimes)

    print()
    print(title)
    print(formatFuncCall(func, *args, **kwargs))
    term.table(
        [
            ["Multi", "Thread" if thread else "Process"],
            ["Number", number],
            ["Concurrency", concurrency],
            [],
            ["Cost Time:"],
            ["Total", "{}ms".format(totalTime)],
            ["Average", "{}ms".format(avgTime)],
            ["Min", "{}ms".format(minTime)],
            ["Max", "{}ms".format(maxTime)],
        ]
    )

    print()
    print("Percentage of the tests served within a certain time:")
    term.table(
        [
            [
                "{}%".format(int(mp * 100)),
                "{}ms".format(costTimes[math.floor(number * mp) - 1]),
            ]
            for mp in markPercentages
        ]
    )

    return {
        "results": results,
        "cost": {
            "total": totalTime,
            "average": avgTime,
            "min": minTime,
            "max": maxTime,
        },
    }
