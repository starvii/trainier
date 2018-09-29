#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List

from trainier.dao.model import Result
from trainier.dao.orm import Session
from trainier.util.logger import logger


class TakeService:
    @staticmethod
    def save(results: List[Result]) -> None:
        session: Session = Session()
        try:
            for result in results:
                session.add(result)
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(e)
        finally:
            session.close()
