# -*- coding: utf-8 -*-

# pyKlf200 - Python client implementation of the Velux KLF200 protocol
# Copyright (c) 2019 Florian Hatat
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

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
