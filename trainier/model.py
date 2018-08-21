#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, BLOB
from trainier.orm import Base


class Trunk(Base):
    __tablename__ = 'trunk'

    entityId = Column(String(20), primary_key=True)
    enTrunk = Column(String)
    cnTrunk = Column(String)
    comment = Column(String)


class Option(Base):
    __tablename__ = 'option'

    entityId = Column(String(20), primary_key=True)
    trunkId = Column(String(20))
    enOption = Column(String)
    cnOption = Column(String)
    isTrue = Column(String)
    comment = Column(String)


class Pic(Base):
    __tablename__ = 'pic'

    entityId = Column(String(20), primary_key=True)
    trunkId = Column(String(20))
    title = Column(String)
    data = Column(BLOB)
    orderNum = Column(Integer)
