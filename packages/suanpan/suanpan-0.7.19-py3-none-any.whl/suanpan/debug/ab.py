# coding=utf-8
from __future__ import print_function

import requests

from suanpan import asyncio, debug
from suanpan.utils import term

DEFAULT_MARK_PERCENTAGES = (0.5, 0.66, 0.75, 0.8, 0.9, 0.95, 0.98, 0.99, 1)


def test(
    func,
    number,
    concurrency=1,
    thread=True,
    args=None,
    kwargs=None,
    title="ABTest",
    funcName=None,
    markPercentages=DEFAULT_MARK_PERCENTAGES,
):
    args = args or []
    kwargs = kwargs or {}
    testFunc = lambda x: debug.costCall(func, *args, **kwargs)
    funcName = funcName or func.__name__
    func.__name__ = funcName
    results = asyncio.map(
        testFunc, range(number), workers=concurrency, thread=thread, pbar=title
    )
    roundns = lambda s: round(s * 1000, 3)
    costTimes = sorted(r[0] for r in results)
    totalTime = sum(costTimes)
    avgTime = totalTime / number
    minTime = min(costTimes)
    maxTime = max(costTimes)

    print()
    print(title)
    print(debug.formatFuncCall(func, *args, **kwargs))
    term.table(
        [
            ["Multi", "Thread" if thread else "Process"],
            ["Number", number],
            ["Concurrency", concurrency],
            [],
            ["Cost Time:"],
            ["Total", "{}ms".format(roundns(totalTime))],
            ["Average", "{}ms".format(roundns(avgTime))],
            ["Min", "{}ms".format(roundns(minTime))],
            ["Max", "{}ms".format(roundns(maxTime))],
        ]
    )

    print()
    print("Percentage of the tests served within a certain time:")
    term.table(
        [
            [
                "{}%".format(int(mp * 100)),
                "{}ms".format(roundns(costTimes[int(number * mp) - 1])),
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


def request(
    method,
    url,
    number,
    kwargs=None,
    concurrency=1,
    markPercentages=DEFAULT_MARK_PERCENTAGES,
):
    args = [method, url]
    return test(
        requests.request,
        number=number,
        concurrency=concurrency,
        args=args,
        kwargs=kwargs,
        title="ABTest - Request - {}".format(method.upper()),
        markPercentages=markPercentages,
    )


def get(
    url,
    number,
    params=None,
    kwargs=None,
    concurrency=1,
    markPercentages=DEFAULT_MARK_PERCENTAGES,
):
    args = [url]
    kwargs = kwargs or {}
    kwargs.update(params=params)
    return test(
        requests.get,
        number=number,
        concurrency=concurrency,
        args=args,
        kwargs=kwargs,
        title="ABTest - Request - GET",
        markPercentages=markPercentages,
    )


def post(
    url,
    number,
    data=None,
    json=None,
    kwargs=None,
    concurrency=1,
    markPercentages=DEFAULT_MARK_PERCENTAGES,
):
    args = [url]
    kwargs = kwargs or {}
    kwargs.update(data=data, json=json)
    return test(
        requests.post,
        number=number,
        concurrency=concurrency,
        args=args,
        kwargs=kwargs,
        title="ABTest - Request - POST",
        markPercentages=markPercentages,
    )
