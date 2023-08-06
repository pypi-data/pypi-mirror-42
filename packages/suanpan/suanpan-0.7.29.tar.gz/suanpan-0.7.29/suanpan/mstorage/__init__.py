# coding=utf-8
from __future__ import print_function

import itertools

from suanpan.arguments import Int, String
from suanpan.mstorage.redis import RedisMStorage
from suanpan.proxy import Proxy


class MStorageProxy(Proxy):
    MAPPING = {"redis": RedisMStorage}
    DEFAULT_ARGUMENTS = [String("mstorage-type", default="redis")]
    REDIS_ARGUMENTS = [
        String("mstorage-redis-host", default="localhost"),
        Int("mstorage-redis-port", default=6379),
    ]
    ARGUMENTS = list(itertools.chain(DEFAULT_ARGUMENTS, REDIS_ARGUMENTS))


mstorage = MStorageProxy()
