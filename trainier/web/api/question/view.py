#!/usr/bin/env python
# -*- coding: utf-8 -*-
from concurrent.futures import Executor, ThreadPoolExecutor
from typing import List, Dict

from tornado.concurrent import run_on_executor
from tornado.gen import coroutine
from tornado.httputil import HTTPServerRequest
from tornado.routing import URLSpec

from trainier.util.logger import Log
from trainier.util.value import process_page_parameters, jsonify
from trainier.web.api import BaseHandler


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
            jsn = yield self.query_questions(request.arguments)
        self.finish(jsn)

    @coroutine
    def post(self, *args, **kwargs) -> None:
        request: HTTPServerRequest = self.request
        jsn = yield self.query_questions(request.arguments)
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

    """================================================================================="""

    @run_on_executor
    def query_questions(self, arguments: Dict) -> str:
        page, size, keyword = process_page_parameters(arguments)
        return jsonify([])

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