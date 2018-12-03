#!/usr/bin/env python
# -*- coding: utf-8 -*-
from tornado.gen import coroutine

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
        return super().get(*args, **kwargs)

    @coroutine
    def post(self, *args, **kwargs):
        return super().post(*args, **kwargs)



