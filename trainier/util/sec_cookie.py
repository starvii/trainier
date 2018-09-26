#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
cookie编码解码
"""

import base64
import hashlib
import hmac
import json
import secrets
from typing import Dict

from .chacha20 import chacha20_encrypt


def enc(secret_key: bytes, clear_data: bytes) -> bytes:
    iv: bytes = secrets.token_bytes(8)  # 64(8)
    sk: bytes = hashlib.sha256(secret_key).digest()  # 256(32)
    c: bytes = chacha20_encrypt(clear_data, sk, iv)
    h: bytes = hmac.digest(secret_key, c + iv, hashlib.sha256)
    ret: bytes = iv + h + c
    return ret


def dec(secret_key: bytes, encoded_data: bytes) -> bytes:
    iv: bytes = encoded_data[:8]
    h: bytes = encoded_data[8:40]
    c: bytes = encoded_data[40:]
    # verify
    hv: bytes = hmac.digest(secret_key, c + iv, hashlib.sha256)
    if h != hv:
        raise ValueError('HMAC verify failed.')
    sk: bytes = hashlib.sha256(secret_key).digest()  # 256(32)
    ret: bytes = chacha20_encrypt(c, sk, iv)
    return ret


class Codec:
    def __init__(self, secret_key: bytes) -> None:
        self.secret_key = secret_key

    def enc_dict(self, _dict: Dict) -> str:
        j: bytes = json.dumps(_dict, separators=(',', ':')).encode()
        c: bytes = enc(self.secret_key, j)
        b: bytes = base64.urlsafe_b64encode(c)
        return b.decode()

    def dec_dict(self, cookie: str) -> Dict:
        c: bytes = base64.urlsafe_b64decode(cookie.encode())
        j: bytes = dec(self.secret_key, c)
        d: Dict = json.loads(j)
        return d
