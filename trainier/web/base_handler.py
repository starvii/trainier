from tornado.web import RequestHandler, StaticFileHandler, RedirectHandler


def default_headers(handler: RequestHandler) -> None:
    handler.set_header('Server', 'Apache/2.2.15 (CentOS)')
    handler.set_header('X-Powered-By', 'PHP/5.2.2')


class StaticHandler(StaticFileHandler):
    def set_default_headers(self):
        default_headers(self)


class HtmlHandler(StaticHandler):
    def parse_url_path(self, url_path):
        if not url_path or url_path.endswith('/'):
            url_path += 'index.html'
        return super(HtmlHandler, self).parse_url_path(url_path)


class IndexHandler(RedirectHandler):
    def set_default_headers(self):
        default_headers(self)


class BaseHandler(RequestHandler):
    def set_default_headers(self):
        default_headers(self)
        self.set_header('Content-Type', 'application/json')

    def not_found(self):
        default_headers(self)
        self.set_header('Content-Type', 'text/html')
        self.set_status(404, 'Not Found')
        self.write('<html><title>404: Not Found</title><body>404: Not Found</body></html>')
        self.finish()


class AuthHandler(BaseHandler):
    pass
