#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
import binascii
from flask import Flask, render_template, request
from trainier import get_flask_app

from trainier.logger import logger

app: Flask = get_flask_app()


@app.route('/question/', methods=('GET',))
def index() -> str:
    return render_template('question/index.html')


@app.route('/question/edit', methods=('GET',))
def edit() -> str:
    entity_id: str = request.args.get('id')
    if entity_id is not None and len(entity_id.strip()) > 0:
        _: bytes = binascii.unhexlify(entity_id.strip())
        entity_id = base64.urlsafe_b64encode(_).decode()
    else:
        entity_id = ''
    return render_template('question/edit.html', entity_id=entity_id)


@app.route('/question/view', methods=('GET',))
def view() -> str:
    entity_id: str = request.args.get('id')
    if entity_id is not None and len(entity_id.strip()) > 0:
        _: bytes = binascii.unhexlify(entity_id.strip())
        entity_id = base64.urlsafe_b64encode(_).decode()
    else:
        entity_id = ''
    return render_template('question/view.html', entity_id=entity_id)
