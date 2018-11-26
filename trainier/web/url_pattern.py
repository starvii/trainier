from typing import List

from tornado.routing import URLSpec

from trainier.config import AppConfig
from trainier.web.api.question.view import urls as question_urls
from web.base_handler import StaticHandler, HtmlHandler

urls: List[URLSpec] = \
    question_urls + \
[
    URLSpec(r'/(.*\.html|.*/)', HtmlHandler, dict(path=AppConfig.HTML)),
    URLSpec(r'/(.*)', StaticHandler, dict(path=AppConfig.STATIC)),
]
