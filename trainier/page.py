#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, render_template
from trainier import get_flask_app

app: Flask = get_flask_app()


@app.route('/question/', methods=('GET',))
def question_index() -> str:
    return render_template('question/index.html')


@app.route('/question/<entity_id>', methods=('GET',))
def question_view(entity_id: str) -> str:
    return render_template('question/view.html')
