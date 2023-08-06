# coding=utf-8
from __future__ import division, print_function

import os
import zipfile

from suanpan import path
from suanpan.log import logger


class LocalStorage(object):

    DEFAULT_IGNORE_KEYWORDS = {"__MACOSX", ".DS_Store"}

    def __init__(self, localTempStore="/tmp", **kwargs):
        self.delimiter = os.sep
        self.tempStore = localTempStore

    def download(self, name, path):
        return self.pathJoin(self.tempStore, path)

    def upload(self, name, path):
        return path

    def walk(self, folderName):
        root = self.pathJoin(self.tempStore, folderName)
        return os.walk(root)

    def listAll(self, folderName):
        root = self.pathJoin(self.tempStore, folderName)
        return (self.pathJoin(root, p) for p in os.listdir(root))

    def listFolders(self, folderName):
        return (p for p in self.listAll(folderName) if os.path.isdir(p))

    def listFiles(self, folderName):
        return (p for p in self.listAll(folderName) if os.path.isfile(p))

    def isFile(self, objectName):
        file = self.pathJoin(self.tempStore, objectName)
        return os.path.isfile(file)

    def isFolder(self, folderName):
        folder = self.pathJoin(self.tempStore, folderName)
        return os.path.isdir(folder)

    def getPathInTempStore(self, path, tempStore=None):
        tempStore = tempStore or self.tempStore
        return self.pathJoin(tempStore, path)

    def pathJoin(self, *paths, **kwargs):
        return os.path.join(*paths)

    def relativePath(self, path, base):
        base = base if base.endswith(self.delimiter) else base + self.delimiter
        return path[len(base) :] if path.startswith(base) else path

    def compress(self, zipFilePath, path, ignore=DEFAULT_IGNORE_KEYWORDS):
        compressFunc = self.compressFolder if os.path.isdir(path) else self.compressFile
        return compressFunc(zipFilePath, path)

    def compressFolder(self, zipFilePath, folderPath, ignore=DEFAULT_IGNORE_KEYWORDS):
        if folderPath in ignore:
            logger.info(
                "Ignore compressing folder: {} -> {}".format(folderPath, zipFilePath)
            )
            return zipFilePath

        logger.info("Compressing folder: {} -> {}".format(folderPath, zipFilePath))
        with zipfile.ZipFile(zipFilePath, "w") as zip:
            for root, _, files in os.walk(folderPath):
                for file in files:
                    filePath = os.path.join(root, file)
                    zip.write(filePath, arcname=self.relativePath(filePath, folderPath))
        logger.info("Compressed folder: {} -> {}".format(folderPath, zipFilePath))
        return zipFilePath

    def compressFile(self, zipFilePath, filePath, ignore=DEFAULT_IGNORE_KEYWORDS):
        if filePath in ignore:
            logger.info(
                "Ignore compressing File: {} -> {}".format(filePath, zipFilePath)
            )
            return zipFilePath

        logger.info("Compressing File: {} -> {}".format(filePath, zipFilePath))
        with zipfile.ZipFile(zipFilePath, "w") as zip:
            _, filename = os.path.split(filePath)
            zip.write(filePath, arcname=filename)
        logger.info("Compressed File: {} -> {}".format(filePath, zipFilePath))
        return zipFilePath

    def extract(self, zipFilePath, distPath, ignore=DEFAULT_IGNORE_KEYWORDS):
        logger.info("Extracting zip: {} -> {}".format(zipFilePath, distPath))
        with zipfile.ZipFile(zipFilePath, "r") as zip:
            zip.extractall(distPath)
        self.removeIgnore(distPath, ignore=ignore)
        logger.info("Extracted zip: {} -> {}".format(zipFilePath, distPath))

    def remove(self, *paths):
        return [path.remove(self.pathJoin(self.tempStore, p)) for p in paths]

    def storageUrl(self, bucket, path):
        return "file://" + path

    def removeIgnore(self, path, ignore=DEFAULT_IGNORE_KEYWORDS):
        for root, folders, files in os.walk(path):
            for folder in folders:
                _path = self.pathJoin(root, folder)
                path.remove(_path)
                logger.info("Removed ignore file: {}".format(_path))
            for file in files:
                _path = self.pathJoin(root, file)
                path.remove(_path)
                logger.info("Removed ignore folder: {}".format(_path))

    def copy(self, path, dist):
        _path = self.pathJoin(self.tempStore, path)
        _dist = self.pathJoin(self.tempStore, dist)
        path.copy(_path, _dist)
        return dist
