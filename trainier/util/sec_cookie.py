#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
cookie编码解码
"""

import hmac
import hashlib
import secrets
from . import rc4


def enc(secret_key: bytes, clear_data: bytes) -> bytes:
    token32: bytes = secrets.token_bytes(32)
    enc1: bytes = rc4.enc(token32, clear_data)
    h: bytes = hmac.digest(secret_key, token32 + enc1, hashlib.sha256)
    buf: bytes = token32 + h + enc1
    enc2: bytes = rc4.enc(secret_key, buf)
    return enc2


def dec(secret_key: bytes, encoded_data: bytes) -> bytes:
    enc2: bytes = rc4.enc(secret_key, encoded_data)
    token32: bytes = enc2[:32]
    h0: bytes = enc2[32:64]
    enc1: bytes = enc2[64:]
    h1: bytes = hmac.digest(secret_key, token32 + enc1, hashlib.sha256)
    if h0 != h1:
        raise ValueError('hmac failed.')
    enc0: bytes = rc4.enc(token32, enc1)
    return enc0


# def test():
#     secret_key = b'ALL IN ONE CISSP'
#     data = ''' A cookie is stored on a client’s computer in the form of a text file. Its purpose is to remember and track data pertaining to a client’s usage for better visitor experience and site statistics.以及中文测试'''.encode()
#     x = enc(secret_key, data)
#     import base64
#     print(x)
#     print(base64.urlsafe_b64encode(x))
#     x[100] = x[100] + 1
#     d1 = dec(secret_key, x)
#     print(d1)
#     print(d1.decode())
#
#
# if __name__ == '__main__':
#     test()
