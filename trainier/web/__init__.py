from typing import List

from tornado.routing import URLSpec

from trainier import AppConfig
from trainier.web.api import IndexHandler, StaticHandler
from trainier.web.api.question.view import urls as question_urls

urls: List[URLSpec] = \
    question_urls + \
    [
        URLSpec(r'/', IndexHandler, {'url': '/index.html'}),
        URLSpec(r'/(.*)', StaticHandler, {'path': AppConfig.STATIC}),
    ]