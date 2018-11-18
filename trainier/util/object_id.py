#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, with_statement, absolute_import

import hashlib
import os
import socket
import struct
import sys
import time
from multiprocessing.dummy import Lock

if not sys.version_info > (3,):
    range = xrange

__ALL__ = ["ObjectId"]

class ObjectId:
    _index, = struct.unpack('>I', os.urandom(4))
    _mac = hashlib.md5(socket.gethostname().encode('utf-8')).digest()[:3]
    _lock = Lock()

    @staticmethod
    def gen_id():
        # | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
        # |   TIMESTAMP   |    MAC    |  PID  |   COUNTER   |
        ObjectId._lock.acquire()
        ObjectId._index = (ObjectId._index + 1) & 0xffffff
        counter = struct.pack('>I', ObjectId._index)[1:]
        ObjectId._lock.release()
        timestamp = struct.pack('>I', int(time.time()))
        pid = struct.pack('>H', os.getpid())
        oid = timestamp + ObjectId._mac + pid + counter
        return oid


def test():
    for i in range(10):
        print(repr(ObjectId.gen_id()))


if __name__ == '__main__':
    test()
