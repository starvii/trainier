#!/usr/bin/env python
# -*- coding: utf-8 -*-

import base64
from flask import Blueprint, request, render_template

blueprint: Blueprint = Blueprint('api-question', __name__, url_prefix='/question')


@blueprint.route('/question/', methods=('GET',))
def index() -> str:
    return render_template('question/index.html')


@blueprint.route('/question/edit', methods=('GET',))
def edit() -> str:
    entity_id: str = request.args.get('id')
    if entity_id is not None and len(entity_id.strip()) > 0:
        entity_id = base64.urlsafe_b64encode(entity_id.strip().encode()).decode()
    else:
        entity_id = ''
    return render_template('question/edit.html', entity_id=entity_id)


@blueprint.route('/question/view', methods=('GET',))
def view() -> str:
    entity_id: str = request.args.get('id')
    if entity_id is not None and len(entity_id.strip()) > 0:
        entity_id = base64.urlsafe_b64encode(entity_id.strip().encode()).decode()
    else:
        entity_id = ''
    return render_template('question/view.html', entity_id=entity_id)
