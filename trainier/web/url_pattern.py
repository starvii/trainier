from typing import List

from tornado.routing import URLSpec

from trainier.config import AppConfig
from trainier.web.api.question.view import urls as question_urls
from web.base_handler import StaticHandler

urls: List[URLSpec] = \
    question_urls + \
[
    URLSpec(r'/(.*\.html)', StaticHandler, {'path': AppConfig.HTML}),
    URLSpec(r'/(.*)', StaticHandler, {'path': AppConfig.STATIC}),
]
