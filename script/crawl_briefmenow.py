#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

sys.path.append('../trainier')

import time
import string
from typing import Dict, List
from html.parser import HTMLParser
import requests

from trainier.api.service import ImportService

class Status:
    NONE = 0
    TRUNK = 1

class QuestionParser(HTMLParser):

    def __init__(self, *, convert_charrefs=True):
        super().__init__(convert_charrefs=convert_charrefs)
        self.status: int = Status.NONE
        self.buf:List[str] = None


    def handle_starttag(self, tag, attrs):
        super().handle_starttag(tag, attrs)
        if tag == 'div' and ('class', 'entry-content') in attrs:
            self.status = Status.TRUNK
            self.buf = list()

    def handle_data(self, data):
        super().handle_data(data)
        if self.status == Status.TRUNK:
            self.buf.append(data)

    def handle_endtag(self, tag):
        super().handle_endtag(tag)
        if self.status == Status.TRUNK and tag == 'div':
            self.status = None
            print('\n'.join(self.buf))
            self.buf = None



def main():
    N: int = 1784
    headers: Dict = {
        'Connection': 'keep - alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3416.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'http://comptiaexamtest.com/Security+SY0-401/',
        'Cookie': '_ga=GA1.2.254375900.1535258932; _gid=GA1.2.1262056639.1535258932; _gat=1',
    }
    for i in range(1128, 1129):
        # time.sleep(5)
        url: str = 'http://comptiaexamtest.com/Security+SY0-401/comptia-security-plus-mock-test-Q{}/'.format(i)
        r: requests.Response = requests.get(url, headers=headers)
        html = r.text
        qp: QuestionParser = QuestionParser()
        qp.feed(html)
        result: Dict = None
        try:
            result: Dict = ImportService.split(qp.text)
        except Exception as e:
            sys.stderr.write(str(e))
            open('not.log', 'a').write(str(i) + '\n')
            continue
        result['source'] = qp.source
        result['entityId'] = str(i)
        result['cnTrunk'] = ''
        result['level'] = 0
        result['comment'] = ''
        for j, o in enumerate(result['options']):
            o['trunkId'] = str(i)
            o['entityId'] = '{i}-{a}'.format(i=i, a=string.ascii_uppercase[j])
            o['cnOption'] = ''
            o['comment'] = ''
            o['orderNum'] = 0
        ImportService.saveDict(result)


def test():
    from bs4 import BeautifulSoup
    b = BeautifulSoup(open('d:/tmp/r.txt', 'r').read())
    # a = b.find('div', {'class':'entry-content'})
    a = b.select('div[class="entry-content"] > p')
    print(a)
    trunk = a[0]
    print(trunk)


if __name__ == '__main__':
    test()
    # main()
