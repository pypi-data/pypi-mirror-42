from enum import EnumMeta
from operator import or_ as _or_
from functools import reduce

class SerFlagMeta(EnumMeta):
    def __new__(meta, name, bases, dict):
        "add NONE and ALL psuedo-members to enumeration"
        enumeration = super().__new__(meta, name, bases, dict)
        none_mbr = enumeration(0)
        if len(enumeration):
            all_mbr = enumeration(reduce(_or_, enumeration))
        else:
            all_mbr = none_mbr
        enumeration._member_map_['NONE'] = none_mbr
        enumeration._member_map_['ALL'] = all_mbr
        return enumeration

