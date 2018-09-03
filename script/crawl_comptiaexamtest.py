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

    def __init__(self, cur_url: str) -> None:
        super().__init__()
        self.cur_url = cur_url
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
        self.entry_node: Tag = None
        self.p_list: List[Tag] = None

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
            self.soup = BeautifulSoup(self.html, features="html.parser")
            return True
        except Exception as e:
            logging.error(e)
            return False

    def f0_parse_html(self, html: str):
        self.html = html
        self.soup = BeautifulSoup(self.html, features="html.parser")

    def f1_next_url(self) -> str or None:
        try:
            tag: Tag = self.soup.select_one('div[class="nav-next"] > a')
            self.next_url: str = tag.attrs['href']
            return self.next_url
        except Exception as e:
            logging.error(e)
            return None

    def f2_title(self) -> str or None:
        try:
            tag: Tag = self.soup.select_one('h1[class="entry-title"]')
            self.title: str = tag.get_text(strip=True)
            _: List[str] = self.TITLE_PATTERN.findall(self.title, re.I)
            assert len(_) >= 1
            num: str = _[0].strip()[1:]
            logging.debug(num)
            self.trunk.code = 'C-' + num
            return self.title
        except Exception as e:
            logging.error(e)
            return None

    def f3_entry(self) -> None:
        self.entry_node: Tag = self.soup.select_one('div[class="entry-content"]')
        self.p_list: List[Tag] = self.entry_node.find_all('p', recursive=True)
        buf: List[str] = list()
        for tag in self.p_list:
            text: str = tag.get_text()
            if 'Show Answer' in text and 'Hide Answer' in text:
                continue
            logging.debug(text)
            ts: List[Tag] = tag.find_all('strong')
            if len(ts) == 1:  # 题干
                buf.append(tag.get_text(separator='\n', strip=True))
            elif len(ts) > 1:  # 选项
                self._deal_options(tag)
            # else:
            #     logging.debug('strong? try to debug.')
            ts: List[Tag] = tag.find_all('img')
            if len(ts) == 1:
                self._deal_pic(ts[0])
            elif len(ts) > 1:
                logging.debug('img? try to debug.')
        self.trunk.enTrunk = '\n'.join(buf)

    def f4_analysis(self):
        pass

    def _deal_pic(self, pic_tag: Tag) -> None:
        assert pic_tag.name == 'img'
        n: int = len(self.pics)
        pic: Pic = Pic(
            entityId='',
            trunkId='',
            code=self.trunk.code + '-' + str(n),
            title='',
            data=b'',
            source=pic_tag.attrs['src'],
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
                    t:Tag = el
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
                isTrue=False,
                orderNum=i,
                comment=''
            ))

# class QuestionParser(HTMLParser):
#
#     def __init__(self, *, convert_charrefs=True):
#         super().__init__(convert_charrefs=convert_charrefs)
#         self.status: str = None
#         self._list: List = None
#         self.source = ''
#         self.text = ''
#
#     def handle_starttag(self, tag, attrs):
#         super().handle_starttag(tag, attrs)
#         if tag == 'h1' and ('class', 'entry-title') in attrs:
#             self.status = 'source'
#         elif tag == 'div' and ('class', 'entry-content') in attrs:
#             self.status = 'text'
#             self._list = list()
#
#     def handle_data(self, data):
#         super().handle_data(data)
#         if 'source' == self.status:
#             self.source = data.strip()
#         elif 'text' == self.status:
#             _ = data.strip()
#             self._list.append(_)
#
#     def handle_endtag(self, tag):
#         super().handle_endtag(tag)
#         if tag == 'h1' and self.status == 'source':
#             self.status = None
#         elif tag == 'div' and self.status == 'text':
#             self.status = None
#             self.text = '\n'.join(self._list)


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
    # p.f0_request()
    p.f0_parse_html(open('sample.html', 'r').read())
    p.f1_next_url()
    p.f2_title()
    p.f3_entry()
    logging.info('next_url=%s', p.next_url)
    logging.info('title=%s', p.title)


if __name__ == '__main__':
    test()
    # main()
