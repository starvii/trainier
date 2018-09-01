#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List, Dict, Set
from sqlalchemy.sql import or_
from trainier.orm import Session
from util.object_id import object_id
from trainier.model import Trunk, Option, Pic
from trainier.logger import logger


class QuizService:
    @staticmethod
    def quiz():
        pass