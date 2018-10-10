#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
open('x.html', 'wb').write(requests.get('https://jinshuju.net/f/2FBgZi').content)
"""

import sys
from typing import List

sys.path.append('../')

import re
import logging
import json
from bs4 import BeautifulSoup, Tag

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s')




def test():
    content = open('x.html', 'rb').read().decode()
    soup: BeautifulSoup = BeautifulSoup(content, features="lxml")

    forms: List[Tag] = soup.select("div[class='form-group']")

    for form in forms:
        try:
            data = dict(trunk=dict(
                code='D4_3_',
                entity_id='',
                cn_trunk='',
                en_trunk='',
                level=0,
                comment='',
                analysis='',
                source='https://jinshuju.net/f/2FBgZi',
                options=list()
            ))

            text: str = form.select_one('label').get_text(strip=True)
            print()
            if text in {'CISSP在线学习火热报名中', '姓名', '邮箱', '单项选择', '本次测试只可提交一次，请仔细检查无误后提交。'}:
                continue
            data['trunk']['cn_trunk']: str = text

            node: Tag = [n for n in form.select('div') if
                         'class' in n.attrs and 'field-description' in n.attrs['class']].pop()
            ps: List[Tag] = node.select('p')
            en_trunk = list()
            opts: List[str] = list()
            for i, p in enumerate(ps):
                text = p.get_text(strip=True)
                if re.match('^[A-I]\.\s+', text):
                    opts.append(text[3:].strip())
                else:
                    en_trunk.append(text)
            data['trunk']['en_trunk'] = ''.join(en_trunk)

            choices: List[Tag] = form.select("div[class='choice-description']")
            assert len(opts) == len(choices)
            for i, (opt, choice) in enumerate(zip(opts, choices)):
                option = dict(
                    entity_id='',
                    trunk_id='',
                    en_option=opt,
                    cn_option=choice.get_text(strip=True),
                    is_true=False,
                    order_num=i,
                    comment='',
                )
                data['trunk']['options'].append(option)
            logging.info(data)
            j = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
            j = j.replace('’', "'")
            open('x.txt', 'ab').write(j.encode() + b'\n\n\n\n')
        except Exception as e:
            logging.error('>>>>>>>>>>>>>>>>>>>>>>>>>>')
            logging.error(e)
            logging.error(form)
            logging.error('<<<<<<<<<<<<<<<<<<<<<<<<<<')
            open('x.txt', 'ab').write(str(form).encode() + b'\n\n\n\n')


if __name__ == '__main__':
    test()
    # main()
