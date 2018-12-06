from typing import List

from tornado.routing import URLSpec

from trainier.config import AppConfig
from trainier.web.api.question.view import urls as question_urls
from trainier.web.api.quiz.view import urls as quiz_urls
from trainier.web.api.quiz.take.take_view import urls as take_urls
from trainier.web.base_handler import StaticHandler, HtmlHandler
from trainier.web.upload import UploadHandler

urls: List[URLSpec] = []
urls.extend(question_urls)
urls.extend(take_urls)
urls.extend(quiz_urls)
urls.extend([
    URLSpec(r'/upload', UploadHandler),
    URLSpec(r'/(.*\.html|.*/)', HtmlHandler, dict(path=AppConfig.HTML)),
    URLSpec(r'/(.*)', StaticHandler, dict(path=AppConfig.STATIC)),
])
