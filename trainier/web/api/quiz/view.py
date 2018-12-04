#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import List

from tornado.gen import coroutine
from tornado.httputil import HTTPServerRequest
from tornado.routing import URLSpec

from trainier.util.logger import Log
from trainier.util.value import jsonify
from trainier.web.api.quiz.controller import QuizController
from trainier.web.base_handler import AuthHandler


class QuizHandler(AuthHandler):
    controller: QuizController = QuizController()

    def head(self, *args, **kwargs):
        """ 帮助信息 """
        return super().head(*args, **kwargs)

    def options(self, *args, **kwargs):
        """ 帮助信息 """
        return super().options(*args, **kwargs)

    @coroutine
    def get(self, *args, **kwargs):
        request: HTTPServerRequest = self.request
        if len(args[0]) > 0:
            # select one
            entity_id: str = args[0]
            Log.trainier.debug('get: entity_id = %s', entity_id)
            jsn = yield self.controller.query_quiz(entity_id, request.headers.get('referer'))
        else:
            # select page
            jsn = yield self.controller.query_quizzes(request.arguments, request.body)
        self.finish(jsn)

    @coroutine
    def post(self, *args, **kwargs):
        request: HTTPServerRequest = self.request
        method: str = request.headers.get('X-HTTP-Method-Override')
        if method in {None, 'POST'}:
            jsn = yield self._post()
        elif method == 'PUT':
            jsn = yield self._put(args[0])
        elif method == 'DELETE':
            jsn = yield self._delete(args[0])
        else:
            self.set_status(405)
            jsn = jsonify(dict(result=0, error='no such method'))
        self.finish(jsn)

    @coroutine
    def put(self, *args, **kwargs):
        self._put(args[0])

    @coroutine
    def delete(self, *args, **kwargs):
        self._delete(args[0])

    @coroutine
    def _post(self):
        request: HTTPServerRequest = self.request
        jsn = yield self.controller.query_quizzes(request.arguments, request.body)
        return jsn

    @coroutine
    def _put(self, entity_id: str):
        request: HTTPServerRequest = self.request
        if len(entity_id) > 0:
            # update
            Log.trainier.debug('put: entity_id = %s', entity_id)
            jsn = yield self.controller.modify_quiz(entity_id, request.body)
        else:
            # create
            jsn = yield self.controller.create_quiz(request.body)
        return jsn

    @coroutine
    def _delete(self, entity_id: str):
        Log.trainier.debug('delete: entity_id = %s', entity_id)
        jsn = yield self.controller.delete_quiz(entity_id)
        return jsn


urls: List[URLSpec] = [
    URLSpec(r'/api/quiz/(.*)', QuizHandler),
]


