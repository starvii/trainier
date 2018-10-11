#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import json

from typing import List, Dict

p = r'^\d+\.\s+'
pa = r'^[A-Ja-j]\.\s+'
book = 'OSG7'
chapter = 6
src = 'CISSP Official Study Guide 7th'


def cn():
    p: str = r'^\d+\.'
    p1: str = r'^[A-Ja-j]\.'
    txt: str = open('cna.txt', 'rb').read().decode()
    txt = txt.replace(' ', '').replace('?', '？').replace(',', '，').replace(':', '：')#.replace('(', '（').replace(')', '）')
    nums = [x.strip()[:-1] for x in re.findall(p, txt, flags=re.M)]
    aa = [x.strip() for x in re.split(p, txt, flags=re.M) if len(x.strip()) > 0]
    if len(nums) != len(aa):
        print('cn_nums=', len(nums), 'cn_aa=', len(aa))
        assert False
    l = list()
    for n, e in zip(nums, aa):
        e1 = e.replace('\n', '')
        if not re.match(p1, e1):
            print(n, e1, 'not match', p1)
            assert False
        answer: str = re.findall(p1, e)[0].strip()[0]
        analysis: str = re.split(p1, e1)[1].strip()
        l.append((n, answer, analysis))
    return l


def en():
    p: str = r'^\d+\.\s+'
    p1: str = r'^[A-Ja-j]\.\s+'
    txt: str = open('ena.txt', 'rb').read().decode()
    txt = txt.replace('“', '"').replace('”', '"').replace('–', '-').replace('‐', '-').replace('’', "'")
    nums = [x.strip()[:-1] for x in re.findall(p, txt, flags=re.M)]
    aa = [x.strip() for x in re.split(p, txt, flags=re.M) if len(x.strip()) > 0]
    if len(nums) != len(aa):
        print('en_nums=', len(nums), 'en_aa=', len(aa))
        assert False
    l = list()
    for n, e in zip(nums, aa):
        if not re.match(p1, e):
            print(n, e, 'not match', p1)
            assert False
        answer: str = re.findall(p1, e)[0].strip()[0]
        analysis: str = re.split(p1, e.replace('\n', ' '))[1].strip()
        l.append((n, answer, analysis))
    return l



def test():
    el = en()
    cl = cn()
    if len(el) != len(cl):
        print('len el = ', len(el), 'len cl = ', len(cl))
        assert False
    with open('a.txt', 'wb') as f:
        for e, c in zip(el, cl):
            title = '{} {}\n\n'.format(e[0], e[1].upper())
            f.write(title.encode())
            f.write(e[2].encode() + b'\n\n')
            f.write(c[2].encode() + b'\n\n\n\n')

test()
