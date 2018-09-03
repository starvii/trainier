#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from logging import Logger
import base64
import binascii
from typing import Dict, List, Set
from flask import Blueprint, Response, Request, request, make_response, abort
from sqlalchemy.orm.attributes import InstrumentedAttribute
from trainier.model import Trunk, Option, Pic
from trainier.logger import logger
from trainier.api.service import dict_to_entity, list_to_entities
from trainier.api.question.service import QuestionService
from trainier.api.service import labelify

blueprint: Blueprint = Blueprint('api-quiz', __name__, url_prefix='/api/quiz')

