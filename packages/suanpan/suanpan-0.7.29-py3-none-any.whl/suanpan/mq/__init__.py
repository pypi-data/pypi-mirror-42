# coding=utf-8
from __future__ import print_function

import itertools

from suanpan.arguments import Bool, Int, String
from suanpan.mq.redis import RedisMQ
from suanpan.proxy import Proxy


class MQProxy(Proxy):
    MAPPING = {"redis": RedisMQ}
    DEFAULT_ARGUMENTS = [String("mq-type", default="redis")]
    REDIS_ARGUMENTS = [
        String("mq-redis-host", default="localhost"),
        Int("mq-redis-port", default=6379),
        Bool("mq-redis-realtime", default=False),
    ]
    ARGUMENTS = list(itertools.chain(DEFAULT_ARGUMENTS, REDIS_ARGUMENTS))


mq = MQProxy()
