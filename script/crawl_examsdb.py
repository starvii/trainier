#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

sys.path.append('../trainier')
import re
import time
from typing import List, Set
from bs4 import BeautifulSoup, Tag, PageElement
import requests

from trainier.model import Trunk, Option
from trainier.api.service import ImportService

OPT_TITLE_PATTERN = re.compile(r'^[A-J]{1}\.')


def req(prev_url: str, url: str) -> str:
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": "ga=GA1.2.763264521.1535459804; _gid=GA1.2.1479568416.1535459804; disallowPrepawayBanner=1; _gat_UA-107060707-1=1",
        "DNT": "1",
        "Host": "www.briefmenow.org",
        "Referer": prev_url,
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
    }
    res: requests.Response = requests.get(url, headers=headers)
    return res.text


def parse_html(url: str, html: str) -> (str, Trunk, List[Option]):
    next_url: str = None
    soup: BeautifulSoup = BeautifulSoup(html, features='html.parser')
    try:
        # 提取下一题的链接
        e: PageElement = soup.select_one('div[class="nav-next"] > a')
        if type(e) == Tag:
            t: Tag = e
            if 'href' in t.attrs:
                next_url = t.attrs['href']
        # 提取题干
        entry_node: Tag = soup.select_one('div[class="entry-content"]')
        l = entry_node.find_all('p', recursive=True)
        assert len(l) > 4  # 至少有一个问题加四个答案

        n: int = 0
        for i, e in enumerate(l):
            t: Tag = e
            if not OPT_TITLE_PATTERN.match(t.text.strip()):
                n = i + 1
        buf: List[str] = list()
        for i in range(n):
            t: Tag = l[i]
            buf.append(t.text.strip())

        trunk: Trunk = Trunk(source=url, level=0, comment='', analysis='', cnTrunk='')
        trunk.en_trunk = '\n'.join(buf)

        # 提取正确答案
        corrects: Set[str] = set([_.text.strip()[0] for _ in entry_node.select('p[class="rightAnswer"]')])

        opts: List[str] = list()
        # 提取选项
        for e in l[n:]:
            t = e
            o: str = t.text.replace('Show Answer', '').strip()
            buf: List[str] = [_.strip() for _ in o.split('\n') if len(_.strip()) > 0]
            opts.extend(buf)
        options: List[Option] = list()
        for i, opt in enumerate(opts):
            assert OPT_TITLE_PATTERN.match(opt)
            o: str = opt[2:].strip()
            t: str = opt[0]
            option = Option(enOption=o, isTrue=t in corrects, cnOption='', orderNum=i, comment='')
            options.append(option)
        return next_url, trunk, options
    except Exception as e:
        out = url + ' //////////// ' + str(e) + '\n'
        sys.stderr.write(out)
        sys.stdout.write(out)
        open('not.log', 'a').write(out)
        return next_url, None, None


def main():
    start_url: str = 'http://www.briefmenow.org/comptia/which-of-the-following-should-sara-configure-11/'
    url: str = start_url
    prev_url: str = 'http://www.briefmenow.org/comptia/which-of-the-following-is-the-quickest-way-to-prevent-the-staff-group-from-gaining-access-to-the-payroll-folder-5/'
    while True:
        time.sleep(5)
        html: str = req(prev_url, url)
        _url, trunk, options = parse_html(url, html)
        if trunk is not None:
            ImportService.save(trunk, options)
        if _url is not None:
            prev_url = url
            url = _url
        else:
            print('maybe the last record.')
            break



def test():
    # from bs4 import BeautifulSoup
    html = open('d:/tmp/r.txt', 'r').read()
    print(repr(parse_html('aaa', html)))


if __name__ == '__main__':
    # test()
    main()
