# coding=utf-8
from __future__ import print_function

import functools
import itertools
import time

from suanpan import asyncio
from suanpan.log import logger


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
    title=None,
    funcName=None,
):
    args = args or []
    kwargs = kwargs or {}
    testFunc = lambda x: costCall(func, *args, **kwargs)
    title = title or func.__name__
    funcName = funcName or func.__name__
    func.__name__ = funcName
    results = asyncio.map(
        testFunc, range(number), workers=concurrency, thread=thread, pbar=title
    )
    costTimes = [r[0] for r in results]
    totalTime = sum(costTimes)
    avgTime = totalTime / number
    multiString = "Multi{}".format("Thread" if thread else "Process")
    logger.info("ABTest - {} - {}".format(title, multiString))
    logger.info(formatFuncCall(func, *args, **kwargs))
    logger.info("Number: {}".format(number))
    logger.info("Concurrency: {}".format(concurrency))
    logger.info("Total: {}s".format(totalTime))
    logger.info("Average: {}s".format(avgTime))
    return {"results": results, "total": totalTime, "average": avgTime}
