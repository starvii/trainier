#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import json

from typing import List

p = r'^\d+\.\s+'
pa = r'^[A-J]\.\s+'
book = 'OSG7'
chapter = '0'

def choices(q: str) -> (str, List[str]):
    buf = [x for x in re.split(pa, q, flags=re.M) if len(x.strip()) > 0]
    # num = [m.group() for m in re.finditer(pa, q, flags=re.M)]
    trunk = buf[0].replace('\n', ' ').strip()
    options = [x.replace('\n', ' ').strip() for x in buf[1:]]
    return trunk, options

def test():
    source: str = open('x.txt', 'rb').read().decode()
    source = source.replace('‐', '-')

    buf = [x for x in re.split(p, source, flags=re.M) if len(x.strip()) > 0]
    num = [m.group() for m in re.finditer(p, source, flags=re.M)]
    for n, b in zip(num, buf):
        code = int(n.strip()[:-1])
        code = '{}/{}/{}'.format(book, chapter, code)
        trunk, opts = choices(b)

        options = list()
        for i, opt in enumerate(opts):
            option = dict(
                entity_id='',
                trunk_id='',
                en_option=opt,
                cn_option='',
                is_true=False,
                order_num=i,
                comment='',
            )
            options.append(option)

        trunk = dict(
            entity_id='',
            code=code,
            en_trunk=trunk,
            level=0,
            comment='',
            analysis='',
            source='CISSP Official Study Guide 7th',
            options=options
        )
        r = dict(trunk=trunk)
        j = json.dumps(r, ensure_ascii=False, separators=(',', ':'))
        open('x.json', 'ab').write(j.encode() + b'\n\n\n\n')
test()
