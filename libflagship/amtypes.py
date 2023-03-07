## ------------------------------------------
## Generated by Transwarp
##
## THIS FILE IS AUTOMATICALLY GENERATED.
## DO NOT EDIT. ALL CHANGES WILL BE LOST.
## ------------------------------------------

import struct
import enum
from dataclasses import dataclass, field
import socket

class Zeroes:
    @classmethod
    def parse(cls, p, num):
        body = p[:num]
        assert set(body) - {0} == set()
        return body, p[num:]

    def pack(self, num):
        return b"\x00" * num

class Bytes(bytes):
    @classmethod
    def parse(cls, p, size):
        return p[:size], p[size:]

class String(Bytes):
    @classmethod
    def parse(cls, p, size):
        body, p = super().parse(p, size)
        assert body[-1] == 0
        return body[:-1].decode(), p

    def pack(self, size):
        return self[:size-1].ljust(size, '\x00').encode()

class Array:
    @classmethod
    def parse(cls, p, elem, num):
        res = []
        for _ in range(num):
            item, p = elem.parse(p)
            res.append(item)
        return res, p

    def pack(self, cls):
        return b"".join(cls.pack(e) for e in self)

class IPv4(str):
    @classmethod
    def parse(cls, p):
        addr = p[:4][::-1]
        return cls(socket.inet_ntoa(addr)), p[4:]

    def pack(self):
        return socket.inet_aton(self)[::-1]

class IntType(int):

    size: int
    desc: str

    @classmethod
    def parse(cls, p):
        return cls(struct.unpack(cls.desc, p[:cls.size])[0]), p[cls.size:]

    def pack(self):
        return struct.pack(self.desc, self)

class i8be(IntType):
    desc = ">b"
    size = 1

class i8le(IntType):
    desc = "<b"
    size = 1

i8 = i8be

class u8be(IntType):
    desc = ">B"
    size = 1

class u8le(IntType):
    desc = "<B"
    size = 1

u8 = u8be

class i16be(IntType):
    desc = ">h"
    size = 2

class i16le(IntType):
    desc = "<h"
    size = 2

i16 = i16be

class u16be(IntType):
    desc = ">H"
    size = 2

class u16le(IntType):
    desc = "<H"
    size = 2

u16 = u16be

class i32be(IntType):
    desc = ">i"
    size = 4

class i32le(IntType):
    desc = "<i"
    size = 4

i32 = i32be

class u32be(IntType):
    desc = ">I"
    size = 4

class u32le(IntType):
    desc = "<I"
    size = 4

u32 = u32be
