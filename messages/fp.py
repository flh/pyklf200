# -*- coding: utf-8 -*-

"""
Functional parameters
"""

import struct

class FPValueMetaclass(type):
    def __bytes__(self):
        return self.__bytes__(self)

class FPValue(metaclass=FPValueMetaclass):
    """
    Base class for functional parameter values
    """
    def __bytes__(self):
        raise NotImplementedError

class Relative(FPValue):
    def __init__(self, percentage):
        self.value = percentage

    def __bytes__(self):
        return struct.pack('>H', int(self.value * 0xC800))

class Percent(FPValue):
    def __init__(self, points):
        self.value = points

    def __bytes__(self):
        return struct.pack('>H', int(self.value * (0xD0D0 - 0xC900) +
            0xC900))

class Target(FPValue):
    def __bytes__(self):
        return struct.pack('>H', 0xD100)

class Current(FPValue):
    def __bytes__(self):
        return struct.pack('>H', 0xD200)

class Default(FPValue):
    def __bytes__(self):
        return struct.pack('>H', 0xD300)

class Ignore(FPValue):
    def __bytes__(self):
        return struct.pack('>H', 0xD400)
