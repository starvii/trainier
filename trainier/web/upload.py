#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import json
import uuid
from pathlib import Path
from typing import Dict

from flask import Blueprint, send_from_directory, request, Request, Response, make_response

from trainier import Config

blueprint: Blueprint = Blueprint('upload', __name__, url_prefix='/upload')


def allowed_file(filename: str) -> str:
    if '.' in filename:
        ext: str = filename.rsplit('.', 1)[1]
        if ext in Config.default.ALLOWED_EXTENSIONS:
            return ext
    return ''


@blueprint.route('/<filename>', methods={'GET'})
def uploaded_file(filename):
    return send_from_directory(Config.default.UPLOAD_FOLDER, filename)


@blueprint.route('/', methods={'POST'})
def upload_file(req: Request or None = None) -> Response:
    res: Response = make_response()
    res.content_type = 'application/json; charset=utf-8'
    file = request.files['upload'] if req is None else req.files['upload']
    if file:
        ext: str = allowed_file(file.filename)
        if len(ext) > 0:
            filename: str = base64.b32encode(uuid.uuid4().bytes).replace(b'=', b'').lower().decode() + '.' + ext
            path: str = str(Path(Config.default.UPLOAD_FOLDER) / Path(filename))
            file.save(path)
            file_url = '/upload/' + filename
            dct: Dict = dict(uploaded=True, url=file_url)
        else:
            dct: Dict = dict(uploaded=False, error=dict(message='forbidden extensions'))
    else:
        dct: Dict = dict(uploaded=False, error=dict(message='no file'))
    res.data = json.dumps(dct).encode()
    return res


@blueprint.route('/test/', methods={'GET'})
def test() -> str:
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>Upload File</title>
</head>
<body>
    <h1>图片上传</h1>
    <form method="post" enctype="multipart/form-data" action="/upload/">
         <input type="file" name="upload">
         <input type="submit" value="上传">
    </form>
</body>
</html>
'''
