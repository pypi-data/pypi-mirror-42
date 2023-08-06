# coding=utf-8
from __future__ import print_function

from suanpan.arguments import Arg
from suanpan.mstorage import mstorage
from suanpan.utils import json, npy, pickle, csv


class MStorageArg(Arg):
    def fixArgValue(self, value):
        return (
            value.replace(self.ARG_VALUE_DELIMITER, "_")
            if isinstance(value, str)
            else value
        )


class Pickle(MStorageArg):
    def load(self, args):
        self.value = super(Pickle, self).load(args)
        return self.value

    def format(self, context):
        if self.value:
            self.value = pickle.loads(mstorage.get(self.value))
        return self.value

    def save(self, context, result):
        obj = result.value
        mstorage.set(self.value, pickle.dumps(obj))
        self.logSaved(self.value)
        return self.value


class Any(Pickle):
    pass


class Npy(MStorageArg):
    def format(self, context):
        if self.value:
            self.value = self.getValue()
        return self.value

    def save(self, context, result):
        obj = result.value
        self.setValue(obj)
        self.logSaved(self.value)
        return self.value

    def setValue(self, obj):
        params = npy.dumps(obj)
        npybytes = params.pop("data")
        data = {"md": json.dumps(params), "data": npybytes}
        return mstorage.mset(self.value, data)

    def getValue(self):
        data = mstorage.mget(self.value)
        params = json.loads(data["md"])
        params["data"] = data["data"]
        return npy.loads(params)


class Csv(MStorageArg):
    def setValue(self, dataframe):
        data = csv.dumps(dataframe)
        return mstorage.set(self.value, data)

    def getValue(self):
        data = mstorage.get(self.value)
        return csv.loads(data)


class Table(Csv):
    pass
