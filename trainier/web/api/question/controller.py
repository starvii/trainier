#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from concurrent.futures import Executor, ThreadPoolExecutor
from typing import List, Dict

from playhouse.shortcuts import model_to_dict
from tornado.concurrent import run_on_executor

from trainier.dao.model import Trunk, Option
from trainier.util.logger import Log
from trainier.util.value import process_page_parameters, jsonify
from trainier.web.api import ErrorInQueryError, CannotFindError
from trainier.web.api.question.service import QuestionService


class QuestionController:
    executor: Executor = ThreadPoolExecutor(4)

    @run_on_executor
    def query_questions(self, arguments: Dict, body: bytes) -> str:
        """
        优先使用arguments中的参数（get / post urlencoded），如果没有再采用body中的参数（json），如果再没有则使用默认值
        :param arguments:
        :param body:
        :return:
        """
        try:
            page, size, keyword, body_json = process_page_parameters(arguments, body)
            ids = None
            if body_json and 'ids' in body_json:
                ids = body_json['ids']
            trunks, count = QuestionService.select_trunks(page, size, keyword, ids)
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
    def query_question(self, entity_id: str, referer: str) -> str:
        try:
            trunk: Trunk = QuestionService.select_trunk_by_id(entity_id)
            result: Dict = dict(result=1)
            if 'view.html' in referer:
                trunk_dict: Dict = QuestionService.t2d(trunk, [QuestionService.view_trunk_length])
                result['prev'], result['next'] = QuestionService.select_prev_next_by_id(entity_id)
            else:
                trunk_dict: Dict = QuestionService.t2d(trunk)
            result['trunk'] = trunk_dict
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
            trunk: Trunk = QuestionService.dict_to_trunk(trunk_dict)
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
            trunk: Trunk = QuestionService.dict_to_trunk(trunk_dict)
            if trunk.entity_id != entity_id:
                raise ValueError(f'entity_id from url {entity_id} is not equal to json {trunk.entity_id}')
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


