#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
rc4算法，需要兼容py2与py3
"""

from __future__ import print_function

import sys

if sys.version_info.major < 3:
    range = xrange


def enc(key, data):
    assert type(key) == bytes or type(key) == bytearray
    assert type(data) == bytes or type(data) == bytearray
    # init s-box
    n = 256
    key_len = len(key)
    sbox = [i for i in range(n)]
    j = 0
    for i in range(n):
        j = (j + sbox[i] + key[i % key_len]) % n
        sbox[i], sbox[j] = sbox[j], sbox[i]

    i = j = 0
    buf = list()
    for b in data:
        i = (i + 1) % n
        j = (j + sbox[i]) % 256
        sbox[i], sbox[j] = sbox[j], sbox[i]
        k = sbox[(sbox[i] + sbox[j]) % n]
        buf.append(b ^ k)
    return bytearray(buf)
