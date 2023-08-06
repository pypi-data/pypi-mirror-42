# coding=utf-8
from __future__ import print_function

import itertools

from suanpan import interfaces
from suanpan.components import Component
from suanpan.dw import dw
from suanpan.log import logger
from suanpan.storage import storage


class DockerComponent(Component, interfaces.HasLogger, interfaces.HasBaseServices):
    ENABLED_BASE_SERVICES = {"dw", "storage"}
    defaultArguments = list(itertools.chain(dw.ARGUMENTS, storage.ARGUMENTS))

    def initBase(self, args):
        logger.setLogger(self.name)
        self.setBaseServices(args)
