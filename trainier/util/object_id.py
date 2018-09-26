#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, with_statement, absolute_import

import base64
import hashlib
import os
import struct
import time
import uuid
from multiprocessing.dummy import Lock

__ALL__ = ["ObjectId"]


class ObjectId:
    _index, = struct.unpack('>I', os.urandom(4))
    _mac = hashlib.md5(struct.pack('>Q', uuid.getnode())[2:]).digest()[:3]
    _lock = Lock()

    @staticmethod
    def gen_id():
        # 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11
        #   TIMESTAMP   |    MAC    |  PID  |   COUNTER
        ObjectId._lock.acquire()
        ObjectId._index = (ObjectId._index + 1) & 0xffffff
        counter = struct.pack('>I', ObjectId._index)[1:]
        ObjectId._lock.release()
        timestamp = struct.pack('>I', int(time.time()))
        pid = struct.pack('>H', os.getpid())
        oid = timestamp + ObjectId._mac + pid + counter
        return oid


def object_id():
    return base64.b16encode(ObjectId.gen_id()).decode().lower()
