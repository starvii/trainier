#!/usr/bin/env python
# -*- coding: utf-8 -*-
from concurrent.futures import Executor, ThreadPoolExecutor
from typing import List, Dict

from playhouse.shortcuts import model_to_dict
from tornado.concurrent import run_on_executor
from tornado.gen import coroutine
from tornado.httputil import HTTPServerRequest
from tornado.routing import URLSpec

from dao.model import Trunk
from trainier.util.logger import Log
from trainier.util.value import process_page_parameters, jsonify
from web.api.question.service import QuestionService
from web.base_handler import BaseHandler


class QuestionHandler(BaseHandler):
    executor: Executor = ThreadPoolExecutor(4)

    @coroutine
    def get(self, *args, **kwargs) -> None:
        if len(args[0]) > 0:
            # select one
            entity_id: str = args[0]
            Log.trainier.debug('get: entity_id = %s', entity_id)
            jsn = yield self.query_question(entity_id)
        else:
            # select page
            request: HTTPServerRequest = self.request
            jsn = yield self.query_questions(request.arguments, request.body)
        self.finish(jsn)

    @coroutine
    def post(self, *args, **kwargs) -> None:
        request: HTTPServerRequest = self.request
        jsn = yield self.query_questions(request.arguments, request.body)
        self.finish(jsn)

    @coroutine
    def put(self, *args, **kwargs) -> None:
        request: HTTPServerRequest = self.request
        if len(args[0]) > 0:
            # update
            entity_id = args[0]
            Log.trainier.debug('get: entity_id = %s', entity_id)
            jsn = yield self.modify_question(request.body)
        else:
            # create
            jsn = yield self.create_question(request.body)
        self.finish(jsn)

    @coroutine
    def delete(self, *args, **kwargs) -> None:
        entity_id = args[0]
        Log.trainier.debug('delete: entity_id = %s', entity_id)
        jsn = yield self.delete_question()
        self.finish(jsn)

    #=================================================================================

    @run_on_executor
    def query_questions(self, arguments: Dict, body: bytes) -> str:
        """
        优先使用arguments中的参数（urlencoded），如果没有再采用body中的参数（json）
        :param arguments:
        :param body:
        :return:
        """
        page, size, keyword = process_page_parameters(arguments, body)
        trunks, count = QuestionService.select_trunks(page, size, keyword, None)
        trunks_list: List[Dict] = [model_to_dict(t, only={
            Trunk.entity_id,
            Trunk.code,
            Trunk.en_trunk,
            Trunk.cn_trunk,
        }) for t in trunks]
        if trunks is not None:
            result: Dict = dict(
                result=1,
                trunks=trunks_list,
                count=count,
            )
        else:
            result: Dict = dict(
                result=0,
                error='query failed'
            )
        return jsonify(result)

    @run_on_executor
    def query_question(self, entity_id: str) -> str:
        pass

    @run_on_executor
    def create_question(self, http_body: bytes) -> str:
        pass

    @run_on_executor
    def modify_question(self, http_body: bytes) -> str:
        pass

    @run_on_executor
    def delete_question(self, entity_id: str) -> str:
        Log.trainier.debug('delete: entity_id = %s', entity_id)
        return jsonify(dict(
            result=0,
            error='NotImplementedError',
        ))


urls: List = [
    URLSpec(r'/api/question/(.*)', QuestionHandler),
]


def test():
    print(urls)


if __name__ == '__main__':
    test()
