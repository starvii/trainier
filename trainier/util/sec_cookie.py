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
import zlib
from typing import Dict

from trainier.util import rc4


def _enc(secret_key: bytes, clear_data: bytes):
    iv: bytes = secrets.token_bytes(8)
    sk: bytes = hmac.digest(iv, secret_key, hashlib.sha256)
    c: bytes = rc4.enc(sk, clear_data)
    h: bytes = hmac.digest(secret_key, c + iv, hashlib.sha256)
    return iv + h + c


def _dec(secret_key: bytes, encrypted_data: bytes):
    iv: bytes = encrypted_data[:8]
    h: bytes = encrypted_data[8:40]
    c: bytes = encrypted_data[40:]
    hv: bytes = hmac.digest(secret_key, c + iv, hashlib.sha256)
    if h != hv:
        raise ValueError('HMAC verify failed.')
    sk: bytes = hmac.digest(iv, secret_key, hashlib.sha256)
    return rc4.enc(sk, c)


class Codec:
    def __init__(self, secret_key: bytes) -> None:
        self.secret_key = secret_key

    def enc_dict(self, _dict: Dict) -> str:
        j: bytes = json.dumps(_dict, separators=(',', ':')).encode()
        z: bytes = zlib.compress(j, zlib.Z_BEST_COMPRESSION)
        c: bytes = _enc(self.secret_key, z)
        b: bytes = base64.urlsafe_b64encode(c)
        return b.decode()

    def dec_dict(self, cookie: str) -> Dict:
        c: bytes = base64.urlsafe_b64decode(cookie.encode())
        z: bytes = _dec(self.secret_key, c)
        j: bytes = zlib.decompress(z)
        d: Dict = json.loads(j)
        return d
