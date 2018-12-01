#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import List

from tornado.gen import coroutine
from tornado.httputil import HTTPServerRequest
from tornado.routing import URLSpec

from trainier.util.logger import Log
from web.api.question.controller import QuestionController
from web.base_handler import BaseHandler


class QuestionHandler(BaseHandler):
    controller: QuestionController = QuestionController()

    @coroutine
    def get(self, *args, **kwargs) -> None:
        request: HTTPServerRequest = self.request
        if len(args[0]) > 0:
            # select one
            entity_id: str = args[0]
            Log.trainier.debug('get: entity_id = %s', entity_id)
            jsn = yield self.controller.query_question(entity_id, request.headers.get('referer'))
        else:
            # select page
            jsn = yield self.controller.query_questions(request.arguments, request.body)
        self.finish(jsn)

    @coroutine
    def post(self, *args, **kwargs) -> None:
        request: HTTPServerRequest = self.request
        jsn = yield self.controller.query_questions(request.arguments, request.body)
        self.finish(jsn)

    @coroutine
    def put(self, *args, **kwargs) -> None:
        request: HTTPServerRequest = self.request
        if len(args[0]) > 0:
            # update
            entity_id = args[0]
            Log.trainier.debug('get: entity_id = %s', entity_id)
            jsn = yield self.controller.modify_question(entity_id, request.body)
        else:
            # create
            jsn = yield self.controller.create_question(request.body)
        self.finish(jsn)

    @coroutine
    def delete(self, *args, **kwargs) -> None:
        entity_id = args[0]
        Log.trainier.debug('delete: entity_id = %s', entity_id)
        jsn = yield self.controller.delete_question(entity_id)
        self.finish(jsn)


urls: List = [
    URLSpec(r'/api/question/(.*)', QuestionHandler),
]
