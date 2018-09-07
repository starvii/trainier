#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

sys.path.append('../')
import re
import time
from typing import List, Set, Dict
from bs4 import BeautifulSoup, Tag, PageElement
import requests

from dao.model import Trunk, Option
from trainier.util.object_id import object_id
from web.question.service import QuestionService

OPT_PATTERN = re.compile(r'[A-J]\.\n')
OPT_EXP_PATTERN = re.compile(r'\n[A-J]\.\n|\nExplanation:\n')
ID_PREFIX = 'B5-'


def req(prev_url: str, url: str) -> str:
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Cookie": "_ga=GA1.2.763264521.1535459804; _gid=GA1.2.1479568416.1535459804; disallowPrepawayBanner=1; _gat_UA-107060707-1=1",
        "DNT": "1",
        "Host": "www.briefmenow.org",
        "Referer": prev_url,
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
    }
    res: requests.Response = requests.get(url, headers=headers)
    return res.text


class QuestionParser:

    def __init__(self, num: int, url: str, html: str) -> None:
        self.html: str = html
        self.soup: BeautifulSoup = BeautifulSoup(html, features='html.parser')
        self.num: int = num
        self.entry_node = None
        self.p_list = None
        self.has_img: bool = False
        self.option_start: int = -1
        self.analysis_start: int = -1
        self.trunk = Trunk(
            entityId=ID_PREFIX + str(num),
            source=url,
            enTrunk='',
            cnTrunk='',
            analysis='',
            level=0,
            comment=''
        )
        self.options = None

    def extract_split_point(self) -> (int, int) or None:
        try:
            self.entry_node: Tag = self.soup.select_one('div[class="entry-content"]')
            self.p_list = self.entry_node.find_all('p', recursive=True)
            # assert len(self.p_list) > 4  # 至少有一个问题加四个答案
            # 但是11题只录入了3个选项，导致无法采集成功
            n0: int = 0  # 选项开始位置
            n1: int = len(self.p_list)  # 解释开始位置
            last: Tag = self.p_list[0]
            for i, e in enumerate(self.p_list[1:]):
                t: Tag = e
                if len(t.select('a > img')) > 0:
                    self.has_img: bool = True
                txt_now: str = t.get_text(separator='\n', strip=True)
                txt_lst: str = last.get_text(separator='\n', strip=True)
                if OPT_PATTERN.match(txt_now) and (not OPT_PATTERN.match(txt_lst)):
                    n0 = i + 1
                if (not OPT_PATTERN.match(txt_now)) and OPT_PATTERN.match(txt_lst):
                    n1 = i + 1
                    break
                last = t
            self.option_start = n0
            self.analysis_start = n1
            return n0, n1
        except Exception as e:
            print(e)
            raise e

    def extract_trunk(self) -> Trunk or None:
        try:
            buf: List[str] = list()
            for e in self.p_list[:self.option_start]:
                t: Tag = e
                buf.append(t.get_text(separator='\n', strip=True))

            en_trunk = '\n'.join(buf).strip()
            self.trunk.en_trunk = en_trunk
            return self.trunk
        except Exception as e:
            print(e)
            raise e

    def extract_options(self) -> List[Option]:
        try:
            corrects: Set[str] = set(
                [_.get_text(separator='\n', strip=True)[0] for _ in self.entry_node.select('p[class="rightAnswer"]')])
            opts: List[(str, str)] = list()
            cache: Set[str] = set()
            lst: List[PageElement] = self.p_list[self.option_start:self.analysis_start]
            for e in lst:
                tag: Tag = e
                text: str = tag.get_text(separator='\n', strip=True).replace('Show Answer', '').strip()
                text = '\n' + text
                option_chars: List[str] = [_.strip() for _ in OPT_EXP_PATTERN.findall(text) if len(_.strip()) > 0]
                option_texts: List[str] = [_.strip() for _ in OPT_EXP_PATTERN.split(text) if len(_.strip()) > 0]
                assert len(option_chars) == len(option_texts)
                if option_chars[-1].startswith('Ex'):
                    if len(option_chars) == 1:
                        break
                    option_chars = option_chars[:-1]
                    option_texts = option_texts[:-1]

                opt = option_texts[0]

                assert opt not in cache
                cache.add(opt)
                opts.append((option_chars[0][0], opt))
            self.options: List[Option] = list()
            for i, (opt, text) in enumerate(opts):
                option_id = object_id() if len(self.trunk.entity_id) == 24 else self.trunk.entity_id + '-' + opt
                self.options.append(Option(
                    entityId=option_id,
                    trunkId=self.trunk.entity_id,
                    enOption=text,
                    isTrue=opt in corrects,
                    cnOption='',
                    orderNum=i,
                    comment=''
                ))
            return self.options
        except Exception as e:
            print(e)
            raise e

    def extract_analysis(self) -> Trunk:
        try:
            buf: List[str] = list()
            for e in self.p_list[self.analysis_start:]:
                t: Tag = e
                text = t.get_text(separator='\n', strip=True)
                t = ''.join(buf)
                if text not in t:
                    buf.append(text)
            analysis = '\n'.join(buf)
            self.trunk.analysis = analysis
            return self.trunk
        except Exception as e:
            print(e)
            raise e


def parse_html(num: int, url: str, html: str) -> (Trunk, List[Option]):
    q: QuestionParser = QuestionParser(num, url, html)
    try:
        q.extract_split_point()
        q.extract_trunk()
        q.extract_analysis()
        q.extract_options()
        if q.has_img:
            out: str = '\n\n{num} - img - {url}\n\n'.format(
                num=num,
                url=url
            )
            open('not.log', 'a').write(out)
        return q.trunk, q.options
    except Exception as e:
        out: str = '\n\n{num} - {err_type}:{err} - {url}\n\n'.format(
            num=num,
            err_type=type(e),
            err=str(e),
            url=url
        )
        open('not.log', 'a').write(out)
        raise e


def read_list(fn: str = 'list.txt') -> Dict:
    lst: List[str] = [_.strip() for _ in open(fn, 'r').readlines() if len(_.strip()) > 0 and '\t' in _.strip()]
    r: Dict = dict()
    for i, line in enumerate(lst):
        a = line.split('\t')
        num: int = int(a[0])
        url: int = a[1]
        assert num == i + 1
        r[num] = url
    return r


def main():
    r: Dict = read_list()
    for i in range(270, 1775 + 1):
        try:
            url = r[i]
            html = req('http://www.briefmenow.org/comptia/category/exam-sy0-401-comptia-security-certification-update-november-11th-2016/', url)
            trunk, options = parse_html(i, url, html)
            if trunk is not None and options is not None:
                QuestionService.save(trunk, options, None)
            else:
                raise Exception('trunk is None or options is None.')
        except Exception as e:
            print(e)
        time.sleep(5)


def test():
    print(read_list())


if __name__ == '__main__':
    # test()
    main()
