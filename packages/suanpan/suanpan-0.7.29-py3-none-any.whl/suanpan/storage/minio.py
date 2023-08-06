# coding=utf-8
from __future__ import division, print_function

import os
import zipfile

from suanpan import path
from suanpan.log import logger


class MinioStorage(object):

    DEFAULT_IGNORE_KEYWORDS = {"__MACOSX", ".DS_Store"}

    def __init__(self, minioTempStore="/tmp", **kwargs):
        self.delimiter = os.sep
        self.tempStore = minioTempStore

    def download(self, name, path):
        pass

    def upload(self, name, path):
        pass

    def remove(self, *paths):
        pass

    def copy(self, path, dist):
        pass

    def storageUrl(self, bucket, path):
        return "minio://" + path
