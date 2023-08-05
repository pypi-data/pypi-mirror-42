# coding=utf-8
from __future__ import print_function

import functools
import itertools
import time

from suanpan.log import logger


def cost(func):
    @functools.wraps(func)
    def _dec(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        cost = round(end - start, 6)
        paramstring = ", ".join(
            itertools.chain(
                (str(a) for a in args),
                ("{}={}".format(k, v) for k, v in kwargs.items()),
            )
        )
        funcstring = "{}({})".format(func.__name__, paramstring)
        logger.info("{} - {}s".format(funcstring, cost))
        return result

    return _dec
