
from enum import Flag
from operator import or_ as _or_
from functools import reduce
from serflag.serflagmeta import SerFlagMeta

class SerFlag (Flag, metaclass=SerFlagMeta):
    def serialize(self):
        if  self.__class__.ALL in self:
            return ['ALL']
        return [k for k, v in self._member_map_.items() if v != self.__class__(0) and v in self]


    @classmethod
    def deserialize(cls, value):
        if 'ALL' in value:
            return cls.ALL

        return cls(reduce(_or_, (cls[item] for item in value), cls.NONE))




