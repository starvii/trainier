#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from typing import Dict, List, Set, Any

from flask import Blueprint, Response, request, make_response, abort, render_template
from sqlalchemy.orm.attributes import InstrumentedAttribute

from trainier.dao.model import Trunk, Option, Pic
from trainier.util.labelify import dict_to_entity, list_to_entities, labelify
from trainier.util.logger import logger
from trainier.util.value import read_int_json_or_cookie, read_str_json_or_cookie, read_list_json
from trainier.web.question.service import QuestionService

blueprint: Blueprint = Blueprint('question', __name__, url_prefix='/question')

trunk_fields = {
    Trunk.entity_id,
    Trunk.code,
    Trunk.en_trunk,
    Trunk.cn_trunk,
    Trunk.analysis,
    Trunk.source,
    Trunk.level,
    Trunk.comment,
}

option_fields = {
    Option.entity_id,
    # Option.trunk_id,
    Option.code,
    Option.en_option,
    Option.cn_option,
    Option.is_true,
}

pic_fields = {
    Pic.entity_id,
    # Pic.trunk_id,
    Pic.code,
    Pic.name,
    Pic.data,
    Pic.source,
}


class API:
    @staticmethod
    @blueprint.route('/api/', methods={'POST'})
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
    def __trans_trunk_to_dict(trunk: Trunk) -> Dict:
        trunk_dict: Dict = labelify(trunk, trunk_fields)
        pics: List[Pic] = trunk.__dict__.get('_pics')
        if pics:
            pics_dict: Dict = labelify(pics, pic_fields)
            trunk_dict['pics'] = pics_dict
        trunks: List[Trunk] = trunk.__dict__.get('_trunks')
        if trunks is not None and len(trunks) > 0:
            trunk_list: List[Dict] = list()
            for trunk_child in trunks:
                trunk_child_dict: Dict = API.__trans_trunk_to_dict(trunk_child)
                trunk_list.append(trunk_child_dict)
            trunk_dict['trunks'] = trunk_list
        else:
            options: List[Option] = trunk.__dict__.get('_options')
            options_dict: Dict = labelify(options, option_fields)
            trunk_dict['options'] = options_dict
        return trunk_dict

    @staticmethod
    def __trans_dict_to_trunk(trunk_dict: Dict) -> Trunk:
        trunk: Trunk = dict_to_entity(trunk_dict, Trunk(), trunk_fields)
        if 'trunks' in trunk_dict and len(trunk_dict['trunks']) > 0:
            # 存在子问题
            trunk_children_dict: Dict = trunk_dict['trunks']
            trunk_children: List[Trunk] = list()
            trunk.__setattr__('_trunks', trunk_children)
            for trunk_child_dict in trunk_children_dict:
                trunk_child: Trunk = API.__trans_dict_to_trunk(trunk_child_dict)
                trunk_children.append(trunk_child)
        elif 'options' in trunk_dict and len(trunk_dict['options']) > 0:
            options_dict: List[Dict] = trunk_dict['options']
            options: List[Option] = list_to_entities(options_dict, Option(), option_fields)
            trunk.__setattr__('_options', options)
        if 'pics' in trunk_dict and len(trunk_dict['pics']) > 0:
            pics_dict: List[Dict] = trunk_dict['pics']
            pics: List[Pic] = list_to_entities(pics_dict, Pic(), pic_fields)
            trunk.__setattr__('_pics', pics)
        return trunk

    @staticmethod
    @blueprint.route('/api/<entity_id>', methods={'GET'})
    def read(entity_id: str) -> Response:
        """
        GET /api
        :param entity_id: TrunkId
        :return:
        """
        trunk: Trunk = QuestionService.select_trunk_by_id(entity_id)
        if trunk is not None:
            trunk_dict: Dict = API.__trans_trunk_to_dict(trunk)
            r: Dict = dict(
                trunk=trunk_dict,
            )
            res: Response = make_response()
            res.content_type = 'application/json; charset=utf-8'
            res.data = json.dumps(r).encode()
            return res
        else:
            abort(404)

    @staticmethod
    @blueprint.route('/api/upload/<trunk_id>', methods={'POST'})
    def upload(trunk_id: str) -> Response:
        """
        上传图片
        还是使用传统的上传方式好了，格式支持广泛，处理起来也方便
        :return:
        """
        pass

    @staticmethod
    @blueprint.route('/api/upload/<trunk_id>/<pic_id>', methods={'GET'})
    def uploaded_file(trunk_id: str, pic_id: str) -> Any:
        pass

    @staticmethod
    @blueprint.route('/api/', methods={'PUT'})
    def create() -> Response:
        """
        PUT /api

        :return:
        """
        try:
            data: bytes = request.data
            j = json.loads(data)
            trunk_dict: Dict = j['trunk']
            trunk: Trunk = API.__trans_dict_to_trunk(trunk_dict)
            QuestionService.save(trunk)
            res: Response = make_response()
            res.content_type = 'application/json; charset=utf-8'
            res.data = json.dumps(dict(result=True)).encode()
            return res
        except Exception as e:
            logger.error(e)
            abort(500)

    @staticmethod
    @blueprint.route('/api/<entity_id>', methods={'PUT'})
    def modify(entity_id: str) -> Response or None:
        """
        PUT /api/<entity_id>
        :param entity_id:
        :return:
        """
        try:
            data: bytes = request.data
            j = json.loads(data)
            trunk: Trunk = API.__trans_dict_to_trunk(j['trunk'])
            if trunk.entity_id != entity_id:
                abort(404)
                return
            # options = list_to_entities(j['options'], Option())
            # pics = list_to_entities(j['pics'], Pic())

            QuestionService.save(trunk)

            res: Response = make_response()
            res.content_type = 'application/json; charset=utf-8'
            res.data = json.dumps(dict(result=True)).encode()
            return res
        except Exception as e:
            logger.error(e)
            abort(500)

    @staticmethod
    @blueprint.route('/api/<entity_id>', methods={'DELETE'})
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
    @blueprint.route('/', methods={'GET'})
    def view_index() -> str:
        return render_template('question/index.html')

    @staticmethod
    @blueprint.route('/edit', methods={'GET'})
    def view_edit() -> str:
        return render_template('question/edit.html')

    @staticmethod
    @blueprint.route('/view', methods={'GET'})
    def view_view() -> str:
        return render_template('question/view.html')
