#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, with_statement

import sys
from collections import deque

if sys.version_info < (3,):
    range = xrange
    input = raw_input

__ALL__ = ["encode_for_id", "encode", "decode", "PADDING"]


ENCODE_TABLE = b'0123456789ABCDEFGHJKMNPQRSTUWXYZ'
DECODE_TABLE = (-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
                -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
                0, 1, 2, 3, 4, 5, 6, 7, 8, 9, -1, -1, -1, -1, -1, -1, -1, 10, 11, 12, 13, 14, 15, 16, 17, -1, 18,
                19, -1, 20, 21, -1, 22, 23, 24, 25, 26, 27, -1, 28, 29, 30, 31)
PADDING = b'ILOV'


def encode_for_id(in_bytes, with_padding=False):
    """
    从右向左编码
    """
    in_bytes_len = len(in_bytes)
    in_bit_len = in_bytes_len * 8
    if in_bit_len % 5 == 0:
        to_encode_bit_len = in_bit_len
        _in_bytes = bytearray(in_bytes)
        padding = b''
    else:
        to_encode_bit_len = (in_bit_len // 5 + 1) * 5
        _in_bytes = bytearray(b'\x00' + in_bytes)
        padding = PADDING[to_encode_bit_len - in_bit_len - 1]
    out_bytes = deque()
    for i in range(to_encode_bit_len - 1, -1, -5):
        j = i - 4
        idx0 = j // 8
        idx1 = i // 8
        bit0 = j % 8
        bit1 = j % 8
        if idx0 == idx1:
            idx = (_in_bytes[idx0] >> (7 - bit1)) & 0x1f
        else:
            idx = ((_in_bytes[idx0] << (5 - (8 - bit0))) | ((_in_bytes[idx1] >> (7 - bit1)) & 0x1f)) & 0x1f
        out_bytes.appendleft(ENCODE_TABLE[idx])
    if with_padding:
        out_bytes.appendleft(padding)
    return bytes(bytearray(out_bytes))


def encode(in_bytes, with_padding=True):
    in_bytes_len = len(in_bytes)
    in_bit_len = in_bytes_len * 8
    if in_bit_len % 5 == 0:
        to_encode_bit_len = in_bit_len
        _in_bytes = in_bytes
        padding = b''
    else:
        to_encode_bit_len = (in_bit_len // 5 + 1) * 5
        _in_bytes = in_bytes + b'\x00'
        padding = PADDING[to_encode_bit_len - in_bit_len - 1]
    out_bytes = deque()
    for i in range(to_encode_bit_len // 5):
        j = i * 5
        k = j + 4
        idx0 = j // 8
        idx1 = k // 8
        bit0 = j % 8
        bit1 = k % 8
        if idx0 == idx1:
            idx = (_in_bytes[idx0] >> (7 - bit1)) & 0x1f
        else:
            assert idx1 == idx0 + 1
            idx = ((_in_bytes[idx0] << (5 - (8 - bit0))) | ((_in_bytes[idx1] >> (7 - bit1)) & 0x1f)) & 0x1f
        out_bytes.append(ENCODE_TABLE[idx])
    if with_padding:
        out_bytes.append(padding)
    return bytes(bytearray(out_bytes))


def decode(in_bytes):
    padding = in_bytes[-1]
    if padding in PADDING:
        _in_bytes = in_bytes[:-1]
        padding_bit_len = PADDING.index(padding) + 1
    else:
        _in_bytes = in_bytes
        padding_bit_len = 0
    out_bit_len = len(_in_bytes) * 5 - padding_bit_len
    assert out_bit_len % 8 == 0
    out_byte_len = out_bit_len // 8
    out_bytes = list(b'\x00' * (out_byte_len + 1))
    for e_idx, e in enumerate(_in_bytes):
        d = DECODE_TABLE[e]
        assert d != -1
        bit_idx = e_idx * 5
        idx0 = bit_idx // 8
        idx1 = (bit_idx + 4) // 8
        bit0 = bit_idx % 8
        bit1 = (bit_idx + 4) % 8
        if idx0 == idx1:
            out_bytes[idx0] |= d << (7 - bit1)
        else:
            assert idx1 == idx0 + 1
            _ = d >> (7 - bit0)
            out_bytes[idx0] |= d >> (5 - (8 - bit0))
            _ = (d << (7 - bit1)) & 0xff
            out_bytes[idx1] |= (d << (7 - bit1)) & 0xff
    return bytes(bytearray(out_bytes[:-1]))


def test():
    import sys
    sys.path.append('./')
    import object_id
    for _ in range(20):
        x = object_id.ObjectId.gen_id()
        print(repr(encode_for_id(x)))
        print(repr(encode(x, False)))


if __name__ == '__main__':
    test()
