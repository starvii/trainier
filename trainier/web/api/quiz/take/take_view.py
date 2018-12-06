#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from typing import List, Dict

from tornado.httputil import HTTPServerRequest
from tornado.routing import URLSpec

from trainier.dao.model import Quiz
from trainier.util.logger import Log
from trainier.util.value import jsonify
from trainier.web.api.quiz.take.controller import QuizActionController
from trainier.web.base_handler import AuthHandler





class QuizTakeHandler(AuthHandler):
    controller: QuizActionController = QuizActionController()

    def head(self, *args, **kwargs):
        return super().head(*args, **kwargs)

    def options(self, *args, **kwargs):
        return super().options(*args, **kwargs)

    def post(self, *args, **kwargs):
        request: HTTPServerRequest = self.request
        try:
            body: bytes = request.body
            param: Dict = json.loads(body)
            quiz_id: str = param.get('quiz_id')
            if quiz_id is None or len(quiz_id.strip()) == 0:
                raise ValueError('quiz_id is empty')
            quiz: str = self.get_cookie('quiz')
            action: str = param.get('action')
            switch: int or None = param.get('switch')
            submit: Dict or None = param.get('submit')
            if quiz is None or len(quiz.strip()) == 0:
                # 只有quiz_id，没有cookie => start
                t = yield self.controller.quiz_start(quiz_id)
                jsn, cookie = t
                self.set_cookie('quiz', cookie)
            # quiz_id + question_num + cookie => switch
            elif action == 'switch':
                t = yield self.controller.quiz_switch(quiz_id, quiz, switch, submit)
                jsn, cookie = t
                self.set_cookie('quiz', cookie)
            # quiz_id + cookie => submit
            elif action == 'submit':
                t = yield self.controller.quiz_submit(quiz_id, quiz, submit)
                jsn, cookie = t
                self.clear_cookie('quiz')
            elif action == 'quit':
                self.clear_cookie('quiz')
                jsn = jsonify(dict(result=1))
            else:
                jsn = dict(result=0, error=dict(message='not allowed action'))
        except Exception as e:
            Log.trainier.error(e)
            jsn: str = dict(result=0, error=dict(message=str(e)))
        self.finish(jsn)


urls: List[URLSpec] = [
    URLSpec(r'/api/quiz/take', QuizTakeHandler),
]