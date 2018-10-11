#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import json

from typing import List, Dict

p = r'^\d+\.\s+'
pa = r'^[A-Ja-j]\.\s+'
book = 'OSG7'
chapter = 5
src = 'CISSP Official Study Guide 7th'

def choices_en(q: str) -> (str, List[str]):
    buf = [x for x in re.split(pa, q, flags=re.M) if len(x.strip()) > 0]
    # num = [m.group() for m in re.finditer(pa, q, flags=re.M)]
    trunk = buf[0].replace('\n', ' ').strip()
    options = [x.replace('\n', ' ').strip() for x in buf[1:]]
    return trunk, options

def choices_cn(q: str) -> (str, List[str]):
    buf = [x for x in re.split(r'^[A-Za-z]\.', q, flags=re.M) if len(x.strip()) > 0]
    trunk = buf[0].replace('\n', '').strip()
    options = [x.replace('\n', '').strip() for x in buf[1:]]
    return trunk, options

def cn(trunks: List):
    source: str = open('cn.txt', 'rb').read().decode()
    source = source.replace(' ', '').replace('?', '？').replace(',', '，')
    buf = [x for x in re.split(r'^\d+\.', source, flags=re.M) if len(x.strip()) > 0]
    num = [m.group() for m in re.finditer(r'^\d+\.', source, flags=re.M)]
    print(len(buf), len(num), len(trunks))
    assert len(buf) == len(num) == len(trunks)
    for i, (n, b) in enumerate(zip(num, buf)):
        cn_trunk, cn_opts = choices_cn(b)
        # i: int = int(n.strip()[:-1])
        trunk = trunks[i]
        trunk['trunk']['cn_trunk'] = cn_trunk
        if len(trunk['trunk']['options']) != len(cn_opts):
            print(n, len(cn_opts), len(trunk['trunk']['options']))
        assert len(trunk['trunk']['options']) == len(cn_opts)
        for j, opt in enumerate(cn_opts):
            trunk['trunk']['options'][j]['cn_option'] = opt
    return trunks


def en():
    source: str = open('en.txt', 'rb').read().decode()
    source = source.replace('‐', '-').replace('’', "'")

    buf = [x for x in re.split(p, source, flags=re.M) if len(x.strip()) > 0]
    num = [m.group() for m in re.finditer(p, source, flags=re.M)]
    l = list()
    for n, b in zip(num, buf):
        code = int(n.strip()[:-1])
        code = '{}/{}/{}'.format(book, chapter, code)
        trunk, opts = choices_en(b)

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
            cn_trunk='',
            level=0,
            comment='',
            analysis='',
            source=src,
            options=options
        )
        r = dict(trunk=trunk)
        l.append(r)
    return l


def test():
    l = en()
    l = cn(l)
    with open('x.json', 'wb') as f:
        for e in l:
            j = json.dumps(e, ensure_ascii=False, separators=(',', ':')).encode()
            f.write(j + b'\n\n\n\n\n')


test()
