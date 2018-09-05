#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

sys.path.append('../')

import time
import re
import logging
from typing import Dict, List, Set, Pattern, Tuple
import requests
from bs4 import BeautifulSoup, Tag, PageElement, NavigableString
from trainier.api.question.service import QuestionService
from trainier.model import Trunk, Option, Pic

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(filename)s:%(lineno)s - %(name)s - %(message)s')


class QuestionParser:
    TITLE_PATTERN: Pattern = re.compile(r'(?<=Test)\s+Q\d+')
    CORRECT_ANSWER: str = 'Correct Answer:'

    def __init__(self, cur_url: str) -> None:
        super().__init__()
        self.cur_url = cur_url
        self.num = ''
        self.next_url: str = ''
        self.title: str = ''
        self.trunk: Trunk = Trunk(
            entityId='',
            code='',
            enTrunk='',
            cnTrunk='',
            analysis='',
            source=cur_url,
            level=0,
            comment=''
        )
        self.options: List[Option] = list()
        self.pics: List[Pic] = list()

        self.html: str = None
        self.soup: BeautifulSoup = None
        # self.entry_node: Tag = None
        # self.p_list: List[Tag] = None
        self.corrects_tag: Tag = None
        self.corrects: Set[str] = None
        self.options_tag: Tag = None

    def f0_request(self) -> bool:
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
        try:
            r: requests.Response = requests.get(self.cur_url, headers=headers)
            self.html = r.text
            # self.soup = BeautifulSoup(self.html, features="html.parser")
            self.soup = BeautifulSoup(self.html, features="lxml")
            return True
        except Exception as e:
            logging.error(e)
            raise e

    def f0_parse_html(self, html: str):
        self.html = html
        self.soup = BeautifulSoup(self.html, features="lxml")

    def f1_next_url(self) -> str or None:
        try:
            tag: Tag = self.soup.select_one('div[class="nav-next"] > a')
            self.next_url: str = tag.attrs['href']
            return self.next_url
        except Exception as e:
            logging.error(e)
            raise e

    def f2_title(self) -> str or None:
        try:
            tag: Tag = self.soup.select_one('h1[class="entry-title"]')
            self.title: str = tag.get_text(strip=True)
            _: List[str] = self.TITLE_PATTERN.findall(self.title, re.I)
            assert len(_) >= 1
            self.num: str = _[0].strip()[1:]
            # logging.debug(num)
            self.trunk.code = 'C-' + self.num
            return self.title
        except Exception as e:
            logging.error(e)
            raise e

    def f3_entry(self) -> None:
        entry_node: Tag = self.soup.select_one('div[class="entry-content"]')
        p_list: List[Tag] = entry_node.find_all('p', recursive=True)

        # 先做部分分离
        buf_trunk: List[Tag] = list()
        buf_analysis: List[Tag] = list()
        buf: List[Tag] = buf_trunk
        for tag in p_list:
            ts: List[Tag] = tag.find_all('strong')
            if len(ts) > 3:  # 选项
                self.options_tag = tag
                continue
            text: str = tag.get_text(strip=True)
            if 'Show Answer' in text and 'Hide Answer' in text:
                # === 切换buf ===
                buf = buf_analysis
                # === 切换buf ===
                continue
            if text.lower().startswith(self.CORRECT_ANSWER.lower()):
                text = tag.select_one('strong').get_text(strip=True)
                text = text[len(self.CORRECT_ANSWER):].strip()
                self.corrects: Set[str] = set([_.strip() for _ in text.split(',') if len(_.strip()) > 0])
                buf.append(tag.select_one('em').get_text(separator='\n', strip=True))
                continue
            buf.append(tag)

        def deal(tag_buf: List[PageElement]) -> str:
            buffer: List[str] = list()
            for t in tag_buf:
                if type(t) == Tag:
                    _t: Tag = t
                    ti: List[Tag] = _t.find_all('img')
                    if len(ti) == 1:
                        self._deal_pic(_t)
                    elif len(ti) > 1:
                        logging.debug('images? try to debug.')
                    else:
                        buffer.append(_t.get_text(separator='\n', strip=True))
                else:
                    # print(type(t), t)
                    buffer.append(str(t))
                buffer.append('\n')
            return '\n'.join(buffer).strip()

        self.trunk.enTrunk = deal(buf_trunk)
        self.trunk.analysis = deal(buf_analysis)
        self._deal_options(self.options_tag)

    def _deal_pic(self, pic_tag: Tag) -> None:
        img: Tag = pic_tag.select_one('img')
        n: int = len(self.pics)
        pic: Pic = Pic(
            entityId='',
            trunkId='',
            code=self.trunk.code + '-' + str(n),
            title='',
            data=b'',
            source=img.attrs['src'],
            orderNum=n,
            comment=''
        )
        self.pics.append(pic)

    def _deal_options(self, opt_tag: Tag) -> None:
        # logging.debug(opt_tag)
        ts: List[Tag] = opt_tag.find_all('strong')
        d: Dict[Tag, List[PageElement]] = dict()
        for t in ts:
            d[t] = list()
        last: Tag = None
        for t in opt_tag.children:
            if t in d:
                last = t
            else:
                d[last].append(t)
        for i, t in enumerate(ts):
            title: str = t.get_text(strip=True)[0]
            buf: List[str] = list()
            for el in d[t]:
                # print(type(_), _)
                if type(el) == Tag:
                    t: Tag = el
                    buf.append(t.get_text(strip=True))
                elif type(el) == NavigableString:
                    buf.append(str(el).strip())
                else:
                    logging.debug('options? try to debug.')
            text: str = '\n'.join(buf).strip()
            self.options.append(Option(
                entityId='',
                trunkId='',
                code=self.trunk.code + '-' + title,
                enOption=text,
                cnOption='',
                isTrue=title in self.corrects,
                orderNum=i,
                comment=''
            ))


# def main():
#     N: int = 1784
#     headers: Dict = {
#         'Connection': 'keep - alive',
#         'Cache-Control': 'max-age=0',
#         'Upgrade-Insecure-Requests': '1',
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3416.0 Safari/537.36',
#         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
#         'Accept-Encoding': 'gzip, deflate',
#         'Accept-Language': 'en-US,en;q=0.9',
#         'Referer': 'http://comptiaexamtest.com/Security+SY0-401/',
#         'Cookie': '_ga=GA1.2.254375900.1535258932; _gid=GA1.2.1262056639.1535258932; _gat=1',
#     }
#     for i in range(1128, 1129):
#         # time.sleep(5)
#         url: str = 'http://comptiaexamtest.com/Security+SY0-401/comptia-security-plus-mock-test-Q{}/'.format(i)
#         r: requests.Response = requests.get(url, headers=headers)
#         html = r.text
#         qp: QuestionParser = QuestionParser()
#         qp.feed(html)
#         result: Dict = None
#         try:
#             result: Dict = ImportService.split(qp.text)
#         except Exception as e:
#             sys.stderr.write(str(e))
#             open('not.log', 'a').write(str(i) + '\n')
#             continue
#         result['source'] = qp.source
#         result['entityId'] = str(i)
#         result['cnTrunk'] = ''
#         result['level'] = 0
#         result['comment'] = ''
#         for j, o in enumerate(result['options']):
#             o['trunkId'] = str(i)
#             o['entityId'] = '{i}-{a}'.format(i=i, a=string.ascii_uppercase[j])
#             o['cnOption'] = ''
#             o['comment'] = ''
#             o['orderNum'] = 0
#         ImportService.save_dict(result)


def test():
    p = QuestionParser('http://comptiaexamtest.com/Security+SY0-401/comptia-security-plus-mock-test-q520/')
    p.f0_request()
    # p.f0_parse_html(open('sample.html', 'r').read())
    p.f1_next_url()
    p.f2_title()
    p.f3_entry()
    logging.info('next_url=%s', p.next_url)
    logging.info('title=%s', p.title)


if __name__ == '__main__':
    test()
    # main()
