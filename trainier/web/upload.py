import base64
from concurrent.futures import Executor
from concurrent.futures.thread import ThreadPoolExecutor
from pathlib import Path
from typing import Dict

from tornado.concurrent import run_on_executor
from tornado.gen import coroutine

from trainier.util.value import jsonify
from trainier.web.base_handler import AuthHandler


class UploadHandler(AuthHandler):
    executor: Executor = ThreadPoolExecutor(4)

    def get(self, *args, **kwargs):
        self.set_header('Content-Type', 'text/html')
        self.finish('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Upload File</title>
</head>
<body>
    <h1>图片上传</h1>
    <form method="post" enctype="multipart/form-data" action="/upload">
         <input type="file" name="upload">
         <input type="submit" value="上传">
    </form>
</body>
</html>
        ''')

    @coroutine
    def post(self, *args, **kwargs):
        if 'upload' not in self.request.files:
            self.finish(jsonify(dict(uploaded=0, error=dict(message='no upload file'))))
            return
        up: Dict = self.request.files['upload'][0]
        n: str = up['filename']
        t: str = up['content_type']
        b: bytes = up['body']
        p: Path = Path(n)
        e: str = p.suffix.lower()
        if e == '.png' and t == 'image/png' and b.startswith(b'\x89PNG'):
            label = 'png'
        elif e in {'.jpg', '.jpeg'} and t == 'image/jpeg' and b.startswith(b'\xFF\xD8\xFF'):
            label = 'jpeg'
        elif e == '.gif' and t == 'image/gif' and b.startswith(b'\x47\x49\x46\x38'):
            label = 'gif'
        else:
            self.finish(jsonify(dict(uploaded=0, error=dict(message='only support png / jpeg / gif format'))))
            return
        # prefix: bytes = f'data:image/{label};base64,'.encode()
        data = yield self.encode_upload(b)
        url: str = f'data:image/{label};base64,{data.decode()}'
        self.finish(jsonify(dict(uploaded=1, url=url)))

    @run_on_executor
    def encode_upload(self, file_bytes: bytes) -> bytes:
        return base64.b64encode(file_bytes)
