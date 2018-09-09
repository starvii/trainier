#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from typing import Dict, List, Set
from flask import Blueprint, Response, request, make_response, abort, render_template
from sqlalchemy.orm.attributes import InstrumentedAttribute
from dao.model import Trunk, Option, Pic
from util.logger import logger
from util.labelify import dict_to_entity, list_to_entities
from web.question.service import QuestionService
from util.labelify import labelify


blueprint: Blueprint = Blueprint('question', __name__, url_prefix='/question')


class API:
    @staticmethod
    @blueprint.route('/api', methods=('POST',))
    @blueprint.route('/api/', methods=('POST',))
    def index_or_create_dispatch() -> Response:
        """
        检查 X-HTTP-Method-Override 字段并根据情况调用 index 还是 create
        :return:
        """
        if 'X-HTTP-Method-Override' in request.headers and request.headers['X-HTTP-Method-Override'] == 'PUT':
            return API.create()
        else:
            return API.index()

    @staticmethod
    @blueprint.route('/api/<entity_id>', methods=('POST',))
    def modify_or_remove_dispatch(entity_id: str) -> Response:
        """
        检查 X-HTTP-Method-Override 字段并根据情况调用 remove 还是 modify
        :param entity_id:
        :return:
        """
        if 'X-HTTP-Method-Override' in request.headers and request.headers['X-HTTP-Method-Override'] == 'DELETE':
            return API.remove(entity_id)
        else:
            return API.modify(entity_id)

    @staticmethod
    @blueprint.route('/api', methods=('POST',))
    @blueprint.route('/api/', methods=('POST',))
    def index() -> Response:
        """
        POST /api
        :param page PageNumber
        :param size PageSize
        :param keyword KeyWord
        :return:
        """
        page: int = 1
        size: int = 10
        keyword: str = ''
        try:
            data: bytes = request.data
            try:
                j: Dict = json.loads(data)
            except json.JSONDecodeError as _:
                j = dict()
            if 'page' in j and type(j['page']) == int:
                page = j['page']
            if 'size' in j and type(j['size']) == int:
                size = j['size']
            if size not in {10, 15, 20, 30, 50, 100}:
                size = 10
            if 'keyword' in j and type(j['keyword']) == str:
                keyword = j['keyword'].strip()
            trunks, c = QuestionService.select_trunks(keyword, page, size)
            if trunks is None or len(trunks) == 0:
                l = []
            else:
                fields: Set[InstrumentedAttribute] = {
                    Trunk.entity_id,
                    Trunk.code,
                    Trunk.en_trunk,
                    Trunk.cn_trunk,
                }
                l: List[Dict] = labelify(trunks, fields)
                # # 数据简化
                # for item in l:
                #     item['en_trunk_full'] = item['en_trunk']
                #     item['cn_trunk_full'] = item['cn_trunk']
                #     if len(item['en_trunk']) > 50:
                #         item['en_trunk'] = item['en_trunk'][:47] + '...'
                #     if len(item['cn_trunk']) > 50:
                #         item['cn_trunk'] = item['cn_trunk'][:47] + '...'
            r: Dict = dict(
                page=page,
                size=size,
                total=c,
                keyword=keyword,
                data=l,
            )
            res: Response = make_response()
            res.content_type = 'application/json; charset=utf-8'
            res.data = json.dumps(r).encode()
            return res
        except Exception as e:
            logger.error(e)
            abort(500)

    @staticmethod
    @blueprint.route('/api/<entity_id>', methods=('GET',))
    def read(entity_id: str) -> Response:
        """
        GET /api
        :param entity_id: TrunkId
        :return:
        """
        _ = QuestionService.select_trunk_options_pics_by_id(entity_id)
        if _ is not None and _[0] is not None:
            trunk, options, pics = _
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
    @blueprint.route('/api', methods=('POST',))
    @blueprint.route('/api/', methods=('POST',))
    def create() -> Response:
        """
        PUT /api
        :return:
        """
        data: bytes = request.data
        j = json.loads(data)
        logger.debug(j)
        trunk: Trunk = Trunk()
        trunk = dict_to_entity(j['trunk'], trunk)
        options = list_to_entities(j['options'], Option())
        pics = list_to_entities(j['pics'], Pic())

        QuestionService.save(trunk, options, pics)

        res: Response = make_response()
        res.content_type = 'application/json; charset=utf-8'
        res.data = json.dumps(dict(result=True)).encode()
        return res

    @staticmethod
    @blueprint.route('/api/<entity_id>', methods=('POST',))
    def modify(entity_id: str) -> Response or None:
        """
        PUT /api/<entity_id>
        :param entity_id:
        :return:
        """
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

    @staticmethod
    @blueprint.route('/api/<entity_id>', methods=('POST',))
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
