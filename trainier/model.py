#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String
from trainier.orm import Base


class UnplannedPort(Base):
    __tablename__ = 'UnplannedPort'

    dbId = Column(Integer, primary_key=True)
    entityId = Column(String(20), unique=True)
    addrRange = Column(String)
    portRange = Column(String)
    reason = Column(String)
    comment = Column(String)