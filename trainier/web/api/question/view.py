#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from concurrent.futures import Executor, ThreadPoolExecutor
from typing import List, Dict

from playhouse.shortcuts import model_to_dict, dict_to_model
from tornado.concurrent import run_on_executor
from tornado.gen import coroutine
from tornado.httputil import HTTPServerRequest
from tornado.routing import URLSpec

from dao.model import Trunk, Option
from trainier.util.logger import Log
from trainier.util.value import process_page_parameters, jsonify
from web.api import ErrorInQueryError, CannotFindError, TrunkIntegrityError
from web.api.question.service import QuestionService
from web.base_handler import BaseHandler


class QuestionHandler(BaseHandler):
    executor: Executor = ThreadPoolExecutor(4)

    @coroutine
    def get(self, *args, **kwargs) -> None:
        if len(args[0]) > 0:
            # select one
            entity_id: str = args[0]
            Log.trainier.debug('get: entity_id = %s', entity_id)
            jsn = yield self.query_question(entity_id)
        else:
            # select page
            request: HTTPServerRequest = self.request
            jsn = yield self.query_questions(request.arguments, request.body)
        self.finish(jsn)

    @coroutine
    def post(self, *args, **kwargs) -> None:
        request: HTTPServerRequest = self.request
        jsn = yield self.query_questions(request.arguments, request.body)
        self.finish(jsn)

    @coroutine
    def put(self, *args, **kwargs) -> None:
        request: HTTPServerRequest = self.request
        if len(args[0]) > 0:
            # update
            entity_id = args[0]
            Log.trainier.debug('get: entity_id = %s', entity_id)
            jsn = yield self.modify_question(entity_id, request.body)
        else:
            # create
            jsn = yield self.create_question(request.body)
        self.finish(jsn)

    @coroutine
    def delete(self, *args, **kwargs) -> None:
        entity_id = args[0]
        Log.trainier.debug('delete: entity_id = %s', entity_id)
        jsn = yield self.delete_question(entity_id)
        self.finish(jsn)

    #=================================================================================

    @run_on_executor
    def query_questions(self, arguments: Dict, body: bytes) -> str:
        """
        优先使用arguments中的参数（urlencoded），如果没有再采用body中的参数（json）
        :param arguments:
        :param body:
        :return:
        """
        try:
            page, size, keyword = process_page_parameters(arguments, body)
            trunks, count = QuestionService.select_trunks(page, size, keyword, None)

            trunks_list: List[Dict] = [model_to_dict(t, only={
                Trunk.entity_id,
                Trunk.code,
                Trunk.en_trunk,
                Trunk.cn_trunk,
            }) for t in trunks]
            result: Dict = dict(
                result=1,
                trunks=trunks_list,
                count=count,
            )
        except ErrorInQueryError as e:
            Log.trainier.error(e)
            result: Dict = dict(
                result=0,
                error='query error'
            )
        except Exception as e:
            Log.trainier.error(e)
            result: Dict = dict(
                result=0,
                error='query error'
            )
        return jsonify(result)

    @run_on_executor
    def query_question(self, entity_id: str) -> str:
        try:
            trunk: Trunk = QuestionService.select_trunk_by_id(entity_id)
            trunk_dict: Dict = self.trunk_to_dict(trunk)
            result: Dict = dict(result=1, trunk=trunk_dict)
        except CannotFindError as e:
            Log.trainier.error(e)
            result: Dict = dict(
                result=0,
                error='cannot find'
            )
        except ErrorInQueryError as e:
            Log.trainier.error(e)
            result: Dict = dict(
                result=0,
                error='query error'
            )
        except Exception as e:
            Log.trainier.error(e)
            result: Dict = dict(
                result=0,
                error='query error'
            )
        return jsonify(result)

    @run_on_executor
    def create_question(self, http_body: bytes) -> str:
        try:
            request_dict: Dict = json.loads(http_body)
            if 'trunk' not in request_dict:
                raise ValueError(f'there is no trunk in http body {http_body}')
            trunk_dict: Dict = request_dict['trunk']
            trunk: Trunk = self.dict_to_trunk(trunk_dict)
            Log.trainier.debug(trunk)
            QuestionService.save(trunk)
            return jsonify(dict(result=1))
        except Exception as e:
            Log.trainier.error(e)
            return jsonify(dict(result=0, error='save error'))

    @run_on_executor
    def modify_question(self, entity_id: str, http_body: bytes) -> str:
        try:
            request_dict: Dict = json.loads(http_body)
            if 'trunk' not in request_dict:
                raise ValueError(f'there is no trunk in http body {http_body}')
            trunk_dict: Dict = request_dict['trunk']
            if trunk_dict.get('entity_id') != entity_id:
                raise ValueError(f'entity_id from url {entity_id} is not equal to json {trunk_dict.get("entity_id")}')
            trunk: Trunk = self.dict_to_trunk(trunk_dict)
            Log.trainier.debug(trunk)
            QuestionService.save(trunk)
            return jsonify(dict(result=1))
        except Exception as e:
            Log.trainier.error(e)
            return jsonify(dict(result=0, error='save error'))

    @run_on_executor
    def delete_question(self, entity_id: str) -> str:
        Log.trainier.debug('delete: entity_id = %s', entity_id)
        return jsonify(dict(
            result=0,
            error='NotImplementedError',
        ))

    @staticmethod
    def trunk_to_dict(trunk: Trunk) -> Dict:
        trunk_dict: Dict = model_to_dict(trunk, exclude={
            Trunk.db_id,
            Trunk.order_num,
            Trunk.parent_id,
            Trunk.en_trunk_text,
            Trunk.cn_trunk_text,
        })
        if len(trunk.__dict__.get('trunks', [])) > 0:
            trunks: List[Trunk] = trunk.__dict__['trunks']
            trunk_list: List[Dict] = list()
            for trunk_child in trunks:
                trunk_child_dict: Dict = QuestionHandler.trunk_to_dict(trunk_child)
                trunk_list.append(trunk_child_dict)
            trunk_dict['trunks'] = trunk_list
        elif len(trunk.__dict__.get('options', [])) > 0:
            options: List[Option] = trunk.__dict__['options']
            options_list: List[Dict] = [model_to_dict(o, exclude={
                Option.db_id,
                Option.trunk_id,
                Option.code,
                Option.order_num,
            }) for o in options]
            trunk_dict['options'] = options_list
        else:
            raise TrunkIntegrityError(None, f'Trunk: {trunk} have something wrong of integrity')
        return trunk_dict

    @staticmethod
    def dict_to_trunk(trunk_dict: Dict) -> Trunk:
        if 'options' in trunk_dict and 'trunks' in trunk_dict:
            raise TrunkIntegrityError(None, f'options and trunks all in trunk dict {trunk_dict}')
        if 'options' not in trunk_dict and 'trunks' not in trunk_dict:
            raise TrunkIntegrityError(None, f'options or trunks not in trunk dict {trunk_dict}')
        trunk: Trunk = dict_to_model(Trunk, trunk_dict, True)
        if 'trunks' in trunk_dict:
            if isinstance(trunk_dict['trunks'], List) and len(trunk_dict['trunks']) > 0:
                trunks: List[Dict] = trunk_dict['trunks']
                trunk.__dict__['trunks'] = [QuestionHandler.dict_to_trunk(t) for t in trunks]
            else:
                raise TrunkIntegrityError(None, f'trunks not correct in trunk dict {trunk_dict}')
        else:
            if isinstance(trunk_dict.get('options'), list) and len(trunk_dict.get('options')) > 0:
                options: List[Dict] = trunk_dict['options']
                trunk.__dict__['options'] = [dict_to_model(Option, o, True) for o in options]
            else:
                raise TrunkIntegrityError(None, f'options not correct in trunk dict {trunk_dict}')
        return trunk

urls: List = [
    URLSpec(r'/api/question/(.*)', QuestionHandler),
]
