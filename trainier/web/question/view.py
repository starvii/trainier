#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from typing import Dict, List, Set
from flask import Blueprint, Response, Request, request, make_response, abort, render_template
from sqlalchemy.orm.attributes import InstrumentedAttribute
from trainier.dao.model import Trunk, Option, Pic
from trainier.util.logger import logger
from trainier.util.labelify import dict_to_entity, list_to_entities, labelify
from trainier.web.question.service import QuestionService
from trainier.util.value import read_int_json_or_cookie, read_str_json_or_cookie, read_list_json


blueprint: Blueprint = Blueprint('question', __name__, url_prefix='/question')


class API:
    @staticmethod
    @blueprint.route('/api/', methods=('POST',))
    def index() -> Response:
        """
        POST /api
        :param page PageNumber
        :param size PageSize
        :param keyword KeyWord
        :return:
        """
        try:
            data: bytes = request.data
            try:
                j: Dict = json.loads(data)
            except json.JSONDecodeError:
                j = dict()
            page = read_int_json_or_cookie('page', j, request, 1)
            size = read_int_json_or_cookie('size', j, request, 10)
            keyword = read_str_json_or_cookie('keyword', j, request, '')
            ids: List[str] = read_list_json('ids', j, None)

            trunks, c = QuestionService.select_trunks(page, size, keyword, ids)
            if trunks is None or len(trunks) == 0:
                lst: List[Dict] = list()
            else:
                fields: Set[InstrumentedAttribute] = {
                    Trunk.entity_id,
                    Trunk.code,
                    Trunk.en_trunk,
                    Trunk.cn_trunk,
                }
                lst: List[Dict] = labelify(trunks, fields)

            r: Dict = dict(
                page=page,
                size=size,
                total=c,
                keyword=keyword,
                data=lst,
            )
            if ids is not None:
                r['ids'] = ids
            res: Response = make_response()
            res.content_type = 'application/json; charset=utf-8'
            res.data = json.dumps(r).encode()
            return res
        except Exception as e:
            logger.error(e)
            abort(500)

    @staticmethod
    @blueprint.route('/api/<entity_id>/', methods=('GET',))
    def read(entity_id: str) -> Response:
        """
        GET /api
        :param entity_id: TrunkId
        :return:
        """
        trunk, options, pics = QuestionService.select_trunk_options_pics_by_id(entity_id)
        if trunk is not None:
            r: Dict = dict(
                trunk=labelify(trunk),
                options=labelify(options),
                pics=labelify(pics)
            )
            res: Response = make_response()
            res.content_type = 'application/json; charset=utf-8'
            res.data = json.dumps(r).encode()
            return res
        else:
            abort(404)

    @staticmethod
    @blueprint.route('/api/', methods=('PUT',))
    def create() -> Response:
        """
        PUT /api
        :return:
        """
        try:
            data: bytes = request.data
            j = json.loads(data)
            trunk: Trunk = Trunk()
            trunk = dict_to_entity(j['trunk'], trunk)
            options = list_to_entities(j['options'], Option())
            pics = list_to_entities(j['pics'], Pic())

            QuestionService.save(trunk, options, pics)

            res: Response = make_response()
            res.content_type = 'application/json; charset=utf-8'
            res.data = json.dumps(dict(result=True)).encode()
            return res
        except Exception as e:
            logger.error(e)
            abort(500)

    @staticmethod
    @blueprint.route('/api/<entity_id>/', methods=('PUT',))
    def modify(entity_id: str) -> Response or None:
        """
        PUT /api/<entity_id>
        :param entity_id:
        :return:
        """
        try:
            data: bytes = request.data
            j = json.loads(data)
            logger.debug(j)
            trunk: Trunk = Trunk()
            trunk = dict_to_entity(j['trunk'], trunk)
            if trunk.entity_id != entity_id:
                abort(404)
                return
            options = list_to_entities(j['options'], Option())
            pics = list_to_entities(j['pics'], Pic())

            QuestionService.save(trunk, options, pics)

            res: Response = make_response()
            res.content_type = 'application/json; charset=utf-8'
            res.data = json.dumps(dict(result=True)).encode()
            return res
        except Exception as e:
            logger.error(e)
            abort(500)

    @staticmethod
    @blueprint.route('/api/<entity_id>/', methods=('DELETE',))
    def remove(entity_id: str) -> Response:
        """
        DELETE /api/<entity_id>
        暂不提供删除功能
        :param entity_id:
        :return:
        """
        pass


class View:
    @staticmethod
    @blueprint.route('/', methods=('GET',))
    def view_index() -> str:
        return render_template('question/index.html')

    @staticmethod
    @blueprint.route('/edit', methods=('GET',))
    def view_edit() -> str:
        return render_template('question/edit.html')

    @staticmethod
    @blueprint.route('/view', methods=('GET',))
    def view_view() -> str:
        return render_template('question/view.html')
