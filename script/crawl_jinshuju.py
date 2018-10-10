#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

sys.path.append('../')

import re
import logging
import json
from lxml import etree

# from trainier.dao.model import Trunk, Option


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s')


def test():
    content = open('x.html', 'rb').read().decode()
    html = etree.HTML(content)
    divs = html.xpath("//div[@class='form-group']")
    # divs = [div for div in divs if 'class' in div.attrib and 'field' in div.attrib['class'].split(' ')]
    for div in divs:
        labels = div.xpath(".//label")
        labels = [label for label in labels if
                  'class' in label.attrib and 'field-label' in label.attrib['class'].split(' ')]
        if len(labels) == 1:
            label = labels.pop()
            cn_trunk = label.text.strip()
            if cn_trunk in {'CISSP在线学习火热报名中', '姓名', '邮箱', '单项选择', '本次测试只可提交一次，请仔细检查无误后提交。'}:
                continue
            data = dict(trunk=dict(
                code='D3-1-X',
                entity_id='',
                cn_trunk=cn_trunk,
                en_trunk='',
                level=0,
                comment='',
                analysis='',
                source='https://jinshuju.net/f/gSq1C6',
                options=list()
            ))

            div_trunk = [f for f in div.xpath(".//div") if
                         'class' in f.attrib and 'field-description' in f.attrib['class'].split(' ')].pop()
            p = div_trunk.xpath(".//p")
            p = [t.text.strip() for t in p if t is not None and t.text is not None]
            # print(len(p), cn_trunk)
            buf = list()
            opts = list()
            for line in p:
                if re.match('^[A-I]\.\s+', line):
                    opts.append(line[3:].strip())
                else:
                    buf.append(line)
            en_trunk = '\n'.join(buf)
            # print(cn_trunk, en_trunk)
            data['trunk']['en_trunk'] = en_trunk
            div_choices = [c for c in div.xpath(".//div[@class='choice-description']")]
            assert len(div_choices) == len(opts)
            for i, opt in enumerate(opts):
                option = dict(
                    entity_id='',
                    trunk_id='',
                    en_option=opt,
                    cn_option=div_choices[i].text.strip(),
                    is_true=False,
                    order_num=i,
                    comment='',
                )
                data['trunk']['options'].append(option)
            print(data)
            open('x.txt', 'a').write(json.dumps(data, ensure_ascii=False, separators=(',', ':')) + '\n\n\n\n')


if __name__ == '__main__':
    test()
    # main()
